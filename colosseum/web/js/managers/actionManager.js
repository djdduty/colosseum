import formToObj from '../tools/formToObj';
import utils from '../utils/utils';

export default class ActionManager {
    constructor(context) {
        this.context = context;
        this.allowTemplates = true;
        this.geocoder = null;
    }

    setGeocoder() {
        this.geocoder = new window.google.maps.Geocoder();
        document.body.removeEventListener('google.maps.loaded', this.setGeocoderCb);
    }

    start() {
        if (process.env.NODE_ENV !== 'production') {
            console.log('ActionManager starting.');
        }

        if (window.googleMapsLoaded) {
            this.setGeocoder();
            return;
        }
        this.setGeocoderCb = this.setGeocoder.bind(this);
        document.body.addEventListener('google.maps.loaded', this.setGeocoderCb);
    }

    bindEvents() {
        document.body.addEventListener('click', this.executeAction.bind(this));
        document.body.addEventListener('submit', this.executeForm.bind(this));
    }

    executeForm(event, geocoded = false) {
        event.stopPropagation();
        event.preventDefault();

        const form = event.target || event.srcElement;
        if (form.action.length === 0) { return; }

        // TODO: Check if it needs to be geocoded
        const data = formToObj(form);


        if (Object.hasOwnProperty.call(data, 'latitude')
        && Object.hasOwnProperty.call(data, 'longitude') && !geocoded) {
            if (!this.geocoder) return;

            // TODO Retrieve properties by class from form instead
            const address = `${data.address}, ${data.city}, ${data.region} ${data.postal}`;
            if (process.env.NODE_ENV !== 'production') {
                console.debug(`Geocoding: ${address}`);
            }

            this.geocoder.geocode({ address }, (results, status) => {
                if (status === window.google.maps.GeocoderStatus.OK) {
                    // results[0].geometry.location;
                    const latIn = form.querySelector('[name=latitude]');
                    const lngIn = form.querySelector('[name=longitude]');
                    if (latIn) latIn.value = results[0].geometry.location.lat();
                    if (lngIn) lngIn.value = results[0].geometry.location.lng();

                    // Recursion! \o/
                    this.executeForm(event, true);
                } else {
                    console.error(`Geocoding failed: ${status}`);
                    window.swal(`Geocode failed: ${status}`);
                }
            });

            return;
        }

        if (form.id !== undefined && form.id.length > 0) {
            const action = new Event(`submit.${form.id}`, { bubbles: true, cancelable: true });
            form.dispatchEvent(action);
        }

        if (Object.keys(data).length === 0) {
            console.warn('Attempted to submit form with no data');
            return;
        }
        const headers = {};
        headers.Accept = 'application/json';

        const request = this.context.request.post(form.action, data, headers);
        request.then(this.formReturned.bind(this, form));
        // this.pendingForm = form;
    }

    formReturned(form, err, text) { // eslint-disable-line
        const response = utils.parseJSON(text);
        if (!response || response === undefined) {
            swal('Warning', // eslint-disable-line no-undef
                'Please refresh and verify that the form was succesful.',
                'warning',
            );
            return;
        }

        // parse action
        if (response.alert) {
            const title = response.alert.title;
            const content = response.alert.content;
            swal(title, content, 'warning'); // eslint-disable-line no-undef
            const action = new Event('form.failure', { bubbles: true, cancelable: true });
            form.dispatchEvent(action);
            return;
        }

        if (response.action) {
            const action = new Event(`action.${response.action}`, { bubbles: true, cancelable: true });
            form.dispatchEvent(action);
        }

        const action = new Event('form.success', { bubbles: true, cancelable: true });
        form.dispatchEvent(action);
    }

    executeAction(event) {
        const e = event || window.event;
        const target = e.target || e.srcElement;

        if (!('action' in target.dataset)) { return; }
        e.stopPropagation();
        e.preventDefault();

        const name = target.dataset.action;
        let action = new Event(`action.${name}`, { bubbles: true, cancelable: true });
        target.dispatchEvent(action);

        if (process.env.NODE_ENV !== 'production') {
            console.debug(`Emitting event 'action.${name}'`, action);
        }

        if (!this.allowTemplates || action.defaultPrevented) return;

        const template = document.getElementById(`action-${name}`);
        if (!template) return;

        const role = template.dataset.role;
        if (!role) { return; }

        let actionName = '';
        switch (role) {
        case 'popup':
            actionName = 'action.openModal';
            break;
        case 'pulldown':
            actionName = 'action.openPulldown';
            break;
        case 'main':
            actionName = 'action.injectTemplate';
            break;
        case 'none':
            return;
        default:
            console.debug(`Found template 'action-${name}' but could not determine the template role`);
            return;
        }

        // console.debug("Emitting template event '"+actionName+"'")
        action = new Event(actionName, { bubbles: true, cancelable: true });
        template.dispatchEvent(action);

        // console.debug("Attempting to use template #"+name);
    }
}

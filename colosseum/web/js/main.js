window['process'] = {env: {NODE_ENV: 'development'}};

import RequestManager from './managers/requestManager';
import NavigationManager from './managers/navigationManager';
import ActionManager from './managers/actionManager';
import DataManager from './managers/dataManager';

/* Controllers */
import heroController from '../../hero/js/controller';

const context = {};

context.navigation = new NavigationManager(context);
context.request = new RequestManager(context);
context.action = new ActionManager(context);
context.data = new DataManager(context);
// context.cookie = new CookieManager(context);

// context.cookie.start();
context.request.start();
context.action.start();
context.data.start();

// Bind controllers and such, BEFORE navigation manager imports initial template
heroController.bind();

context.action.bindEvents();
context.data.bindEvents();
context.navigation.bindEvents();

window.context = context;

document.body.addEventListener('action.reload', reload);
document.body.addEventListener('action.injectTemplate', injectTemplate);

context.navigation.start(); // this has to come after event bindings since it dispatches action.injectTemplate

function reload() {
    context.navigation._navigate(window.location.href); //eslint-disable-line
}

// Generic template events -----------------------------------------------------
function importTemplate(event, target) {
    const template = event.target || event.srcElement;
    if (!template || template.tagName !== 'TEMPLATE' || !target) return false;

    const clone = document.importNode(template.content, true);
    target.appendChild(clone);

    if (template.id) {
        if (process.env.NODE_ENV !== 'production') {
            console.debug(`Inserted template ${template.id}`);
        }

        const inserted = new Event(`template.${template.id}`, { bubbles: true, cancelable: true });
        target.dispatchEvent(inserted);
    }
    return true;
}

function injectTemplate(event) {
    const target = document.getElementsByTagName('main')[0];
    importTemplate(event, target);
}

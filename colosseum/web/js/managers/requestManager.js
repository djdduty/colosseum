import promise from '../tools/promise';

class Progress {
    constructor(name, value = 0, total = 0) { // eslint-disable-line
        this.value = 0;
        this.total = total;

        this.wrapper = document.createElement('div');
        const wrapper = this.wrapper;
        wrapper.id = `${name}-wrapper`;
        wrapper.classList.add('progress');

        this.bar = document.createElement('div');
        const bar = this.bar;
        bar.id = name;
        bar.classList.add('progress-bar');
        wrapper.appendChild(bar);
    }

    attach(target) {
        target.appendChild(this.wrapper);
        return this;
    }

    getValue() {
        return this.value;
    }

    setValue(value) {
        this.value = value;
        this.invalidate();
    }

    getTotal() {
        return this.total;
    }

    setTotal(total) {
        this.total = total;
        this.invalidate();
    }

    getPercentage() {
        if (this.total === 0) return 0;
        return (this.value / this.total) * 100;
    }

    invalidate() {
        if (this.getPercentage() === 0) {
            this.bar.style.display = 'none';
            this.bar.style.width = '0px';
            return;
        }
        this.bar.style.display = 'block';
        this.bar.style.width = this.getPercentage() + '%'; // eslint-disable-line
    }
}

export default class RequestManager {
    constructor() {
        this.progress = new Progress('rq');
    }

    start(context = undefined) {
        this.context = context;
        if (process.env.NODE_ENV !== 'production') {
            console.log('RequestManager starting.');
        }

        if (!document.getElementById('rq')) {
            this.progress.attach(document.body);
        } else {
            this.progress.attach(document.getElementById('rq'));
        }
    }

    debug() {
        this.progress.total = 10;
        this.progress.invalidate();
        for (let i = 0; i < 10; i += 1) {
            setInterval(this.debugInc.bind(this), 1000);
        }
    }

    debugInc() {
        if (!this.progress.total) return;
        if (this.progress.getValue() === this.progress.total) {
            this.progress.setValue(0);
            return;
        }
        this.progress.setValue(this.progress.getValue() + 1);
    }

    post(url, data = null, headers = []) {
        return this.request('POST', url, data, headers);
    }

    get(url, data = null, headers = []) {
        return this.request('GET', url, data, headers);
    }

    request(method, url, data = null, headers = []) {
        headers['X-Requested-With'] = 'XMLHttpRequest'; // eslint-disable-line
        const request = promise.ajax(method, url, data, headers);

        this.progress.setTotal(this.progress.getTotal() + 1);
        request.then(this.requestDone.bind(this));
        return request;
    }

    requestDone() {
        this.progress.setValue(this.progress.getValue() + 1);
        setTimeout(this.clearTick.bind(this), 1000);
    }

    clearTick() {
        if (process.env.NODE_ENV !== 'production') {
            console.log('Clearing stale load state.');
        }
        this.progress.setValue(this.progress.getValue() - 1);
        this.progress.setTotal(this.progress.getTotal() - 1);
    }
}

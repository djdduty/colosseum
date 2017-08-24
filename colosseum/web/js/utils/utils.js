function parseJSON(text) {
    try {
        const parsed = JSON.parse(text);
        return parsed;
    } catch (e) {
        console.error(e);
    }
    return undefined;
}

function parseUriQuery(url) {
    let query = {}; // eslint-disable-line
    const qstr = url.indexOf('?') !== -1 ? url.split('?')[1] : url;
    const a = qstr.split('&');
    for (let i = 0; i < a.length; i += 1) {
        const b = a[i].split('=');
        query[decodeURIComponent(b[0])] = decodeURIComponent(b[1] || '');
    }
    return query;
}

function changeDelay() {
    let timer = 0;
    return (callback, ms) => {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
}

const utils = {
    parseJSON,
    changeDelay,
    parseUriQuery,
};

export default utils;

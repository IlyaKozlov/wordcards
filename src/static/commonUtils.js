function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function getUid() {
    const uid = getQueryParam('uid');
    if (uid !== null) {
        localStorage.setItem('uid', uid);
        return uid;
    } else {
        return localStorage.getItem('uid');
    }
}

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

async function playAudio(url) {
    if (url && url.startsWith( 'http')) {
        const audio = new Audio(url);
        // Try to play the audio; ignore any play errors (e.g., autoplay restrictions)
        let started = true;
        try {
            await audio.play();
            console.log('Audio started playing:', url);
        } catch (err) {
            started = false;
            // Ignore play error
            console.log('Audio play failed for:', url);
        }
        console.log('Audio played:', url);
        // Wait for audio to finish before proceeding only if it started
        if (started) {
        await new Promise(resolve => {
                audio.onended = resolve; // Resolve when audio ends
                audio.onerror = resolve; // Also resolve if an error occurs during playback
        });
            console.log('Audio finished playing:', url);
        }
    }
}


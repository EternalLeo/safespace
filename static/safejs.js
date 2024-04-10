function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function delayframe() {
    return new Promise(resolve => requestAnimationFrame(resolve));
}

async function fadeShrink() {
    let container = document.getElementsByClassName('container')[0];
    let popup = document.getElementsByClassName('popup')[0];

    container.classList.remove('fadein');
    container.classList.add('fadeout');
    await delay(500);
    container.classList.add('hidden');
    popup.classList.remove('hidden');
    await delayframe();
    await delayframe();
    container.classList.add('opzero');
    popup.classList.remove('opzero');
    await delayframe();
    await delayframe();
    popup.classList.remove('fadeout');
    popup.classList.add('fadein');
}

async function backButton(event) {
    event.preventDefault();

    let container = document.getElementsByClassName('container')[0];
    let popup = document.getElementsByClassName('popup')[0];

    popup.classList.add('fadeout');
    popup.classList.remove('fadein');
    await delay(500);
    popup.classList.add('hidden');
    container.classList.remove('hidden');
    await delayframe();
    await delayframe();
    popup.classList.add('opzero');
    container.classList.remove('opzero');
    await delayframe();
    await delayframe();
    container.classList.remove('fadeout');
    container.classList.add('fadein');
}
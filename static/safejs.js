function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function delayframe() {
    return new Promise(resolve => requestAnimationFrame(resolve));
}

async function fadeShrink(buttonid) {
    // Text change + form action
    var popupText = document.getElementById('popup-text');
    var action = document.getElementById('action');
    if (buttonid==1){
        popupText.textContent = 'Log-in';
        action.value = 'login';
    } else if (buttonid==2){
        popupText.textContent = 'Sign-up';
        action.value = 'signup';
    }
    let container = document.getElementsByClassName('container')[0];
    let popup = document.getElementsByClassName('popup')[0];
    // Awful css-js magic to make the animations work
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
    event.preventDefault(); // Act as a back button

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

    // Clear the input fields if back button pressed
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('result-text').textContent = '';
}


document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission to submit on our own terms

        var formData = new FormData(form); // Get form data
        var action = formData.get('action');

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result-text').style.color = 'rgb(216, 68, 68)';
                document.getElementById('result-text').textContent = data.error;
            } else {
                if (action == 'signup') {
                    document.getElementById('result-text').style.color = 'rgb(30, 150, 25)';
                    document.getElementById('result-text').textContent = data.message;
                } else {
                    // Login
                    window.location.href = '/success';
                }
                
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

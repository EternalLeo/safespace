
// FORM
document.addEventListener('DOMContentLoaded', function() {
    var pfpform = document.getElementById('pfpform')
    pfpform.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission to submit on our own terms

        var formData = new FormData(pfpform); // Get form data
        var me = formData.get('me');

        fetch(`/profile/${me}`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('upload-text').style.color = 'rgb(216, 68, 68)';
                document.getElementById('upload-text').textContent = data.error;
            } else {
                document.getElementById('upload-text').style.color = 'rgb(30, 150, 25)';
                document.getElementById('upload-text').textContent = data.message;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

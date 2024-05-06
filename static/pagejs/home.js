// Sort button menu visibility
var dropped = false;
function permadrop(){
    if (dropped){
        dropped = false;
        document.getElementById("sortmenu").style.removeProperty("display");
        document.getElementById("sortbtn").style.backgroundColor = "transparent";
    } else {
        dropped = true;
        document.getElementById("sortmenu").style.display = "flex";
        document.getElementById("sortbtn").style.backgroundColor = "#d9d9d9";
    }
}

// Get the source of the preloaded icons to change sortimg icon.
var sort = 1; // Redundant, in-case I want to store favorite sort type for later.
function changesort(iconID){
    var icon;
    sort = iconID;
    switch (iconID) {
        case 0:
            icon = document.getElementById('timeIcon').src;
            break;
        case 1:
            icon = document.getElementById('heartIcon').src;
            break;
        default:
            sort = 1;
            icon = document.getElementById('heartIcon').src;
    }
    document.getElementById('sortimg').src = icon;
}

// Display remaining character count
var resetflag = 0;
document.getElementById('postinput').addEventListener('input', function () {
    var currentLength = this.value.length;
    document.getElementById('charcount').textContent = currentLength + ' / 1000';
    if (currentLength==1000){
        document.getElementById('charcount').style.color = "rgb(216, 68, 68)"
        resetflag = 1;
    } else if (resetflag == 1) {
        document.getElementById('charcount').style.removeProperty("color")
    }
});

// Display media file name.
document.getElementById('fileInput').addEventListener('change', function () {
    var fileName = this.files[0].name;
    var count = this.files.length
    document.getElementById('fileName').textContent = `${fileName} (${count})`;
});

function heart(self, postid){
    var icon = self.getAttribute('alt');
    if (icon == 'Empty Heart icon') {
        self.src = document.getElementById('heartIcon').src;
        self.alt = 'Heart icon';
        document.getElementById('likeact').value = "heart";
        document.getElementById(`hearts_${postid}`).textContent = Number(document.getElementById(`hearts_${postid}`).textContent) + 1;
    } else {
        self.src = document.getElementById('eheartIcon').src;
        self.alt = 'Empty Heart icon';
        document.getElementById('likeact').value = "unheart";
        document.getElementById(`hearts_${postid}`).textContent -= 1
    }

    document.getElementById('heart_id').value = postid;
    var heartform = document.getElementById('heartform');
    var event = new Event('submit');
    heartform.dispatchEvent(event);
}

// // FORMS

// New post

document.addEventListener('DOMContentLoaded', function() {
    var postform = document.getElementById('postform')
    postform.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission to submit on our own terms

        var formData = new FormData(postform); // Get form data

        fetch('/home', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('charcount').style.color = "rgb(216, 68, 68)";
                document.getElementById('charcount').textContent = data.error;
            } else {
                window.location.href = '/home';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    var heartform = document.getElementById('heartform')
    heartform.addEventListener('submit', function(event) {
        event.preventDefault();

        var formData = new FormData(heartform);

        fetch('/home', {
            method: 'POST',
            body: formData
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});

// Change displayed profile picture after upload
document.getElementById('profile_picture_input').addEventListener('change', function(event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile_picture').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});
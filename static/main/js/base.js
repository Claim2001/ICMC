let popups = Array.from(document.querySelectorAll(".popup-window")),
    closeButtons = Array.from(document.querySelectorAll(".closeButton"));

closeButtons.forEach(function (button) {
    button.addEventListener("click", closePopups);
});

document.addEventListener('keydown', function (evt) {
    if (evt.keyCode === 27) {
        closePopups();
    }
});

function closePopups() {
    popups.forEach(function (popup) {
        popup.style.display = "none";
    });
}

function isAllowedFileFormat(filename) {
    filename = filename.toLowerCase();

    let allowed_extensions = ["jpeg", "png", "jpg", "pdf"],
        extension = filename.split('.').pop();

    return allowed_extensions.includes(extension);
}

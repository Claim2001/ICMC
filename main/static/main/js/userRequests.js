let payButtons = Array.from(document.querySelectorAll(".payButton")),
    payPopup = document.querySelector(".payPopup"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    onlinePayLink = document.querySelector("a.popupBlock#online"),
    bankPayLink = document.querySelector("a.popupBlock#bank"),
    bankPopup = document.querySelector(".bankPopup"),
    fileBox = document.querySelector(".fileBox"),
    fileInput = document.querySelector("input[type='file']"),
    submitButton = document.querySelector("button[type='submit']");


closeButtons.map(function (button) {
    button.addEventListener("click", closePopups);
});

document.addEventListener('keydown', function (evt) {
    if (evt.keyCode === 27) {
        closePopups();
    }
});

function closePopups() {
    payPopup.style.display = "none";
    bankPopup.style.display = "none";
}

payButtons.map(function (button) {
    button.addEventListener("click", function () {
        let id = button.dataset.id;
        onlinePayLink.href = "#" + id;
        document.payForm.action = id.toString();  // TODO: real link
        payPopup.style.display = "block";
    });
});

bankPayLink.addEventListener("click", function (evt) {
    evt.preventDefault();
    closePopups();

    bankPopup.style.display = "block";
});

submitButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    if (isAllowedFileFormat(fileInput.value)) {
        document.payForm.submit();
    }
});

fileBox.addEventListener("click", function () {
    fileInput.click();
});

fileInput.addEventListener("change", function () {
    fileBox.className = isAllowedFileFormat(fileInput.value) ? "popupBlock fileBox filled" : "popupBlock fileBox incorrect";
});

function isAllowedFileFormat(filename) {
    filename = filename.toLowerCase();

    let allowed_extensions = ["jpeg", "png", "jpg", "pdf"],
        extension = filename.split('.').pop();

    return allowed_extensions.includes(extension);
}

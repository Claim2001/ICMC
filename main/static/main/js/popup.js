let removePopupWindow = document.querySelector(".remove-window"),
    techCheckPopupWindow = document.querySelector(".techCheck-window"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    removeOpenButtons = Array.from(document.querySelectorAll(".removeOpenButton")),
    techCheckOpenButtons = Array.from(document.querySelectorAll(".techCheckOpenButton")),
    firstTechCheckLink = document.querySelector("#techCheck"),
    yearTechCheckLink = document.querySelector("#yearTechCheck"),
    removeForm = document.querySelector("#removeForm"),
    fileBox = document.querySelector(".fileBox"),
    fileInput = document.querySelector("input[type='file']"),
    submitButton = document.querySelector("button[type='submit']"),
    bankPopup = document.querySelector(".bankPopup");


removeOpenButtons.map(function (button) {
   button.addEventListener('click', function () {
       let boatID = button.dataset.id;
       removeForm.action = "/requests/" + boatID + "/remove/";

       removePopupWindow.style.display = "flex";
   });
});

let techCheckBoatID = 0;

firstTechCheckLink.addEventListener("click", function (evt) {
    evt.preventDefault();
    openBankPopup("/requests/" + techCheckBoatID + "/techCheck");
});

yearTechCheckLink.addEventListener("click", function (evt) {
    evt.preventDefault();
    openBankPopup("/requests/" + techCheckBoatID + "/yearTechCheck");
});

function openBankPopup() {
    closePopups();
    bankPopup.style.display = "block";
}

techCheckOpenButtons.map(function (button) {
    button.addEventListener('click', function () {
        techCheckBoatID = button.dataset.id;
        techCheckPopupWindow.style.display = "flex"
    });
});

closeButtons.map(function (button) {
    button.addEventListener("click", closePopups);
});

document.addEventListener('keydown', function (evt) {
    if (evt.keyCode === 27) {
        closePopups();
    }
});

submitButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    if (isAllowedFileFormat(fileInput.value)) {
        removeForm.submit();
    }
});

function closePopups() {
    Array.from(document.querySelectorAll(".popup-window")).forEach(function (popup) {
        popup.style.display = "none";
    });
}


fileBox.addEventListener("click", function () {
   fileInput.click();
});

fileInput.addEventListener("change", function () {
    fileBox.className = isAllowedFileFormat(fileInput.value) ? "popupBlock fileBox filled" : "popupBlock fileBox incorrect";
});

function isAllowedFileFormat(filename) {
    filename = filename.toLowerCase();

    let allowed_extensions = ["jpeg", "png", "jpg", "pdf", "docx", "doc"],
        extension = filename.split('.').pop();

    return allowed_extensions.includes(extension);
}

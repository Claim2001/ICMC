let removePopupWindow = document.querySelector(".remove-window"),
    techCheckPopupWindow = document.querySelector(".techCheck-window"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    removeOpenButtons = Array.from(document.querySelectorAll(".removeOpenButton")),
    techCheckOpenButtons = Array.from(document.querySelectorAll(".techCheckOpenButton")),
    techCheckLink = document.querySelector("#techCheck"),
    yearTechCheckLink = document.querySelector("#yearTechCheck"),
    removeForm = document.querySelector("#removeForm"),
    fileBox = document.querySelector(".fileBox"),
    fileInput = document.querySelector("input[type='file']");


removeOpenButtons.map(function (button) {
   button.addEventListener('click', function () {
       let boatID = button.dataset.id;
       removeForm.action = "/requests/" + boatID + "/remove/";

       removePopupWindow.style.display = "flex";
   });
});

techCheckOpenButtons.map(function (button) {
    button.addEventListener('click', function () {
        let boatID = button.dataset.id;
        techCheckLink.href = "/requests/" + boatID + "/techCheck";
        yearTechCheckLink.href = "/requests/" + boatID + "/yearTechCheck";

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

function closePopups() {
    removePopupWindow.style.display = "none";
    techCheckPopupWindow.style.display = "none";
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

let removePopupWindow = document.querySelector(".remove-window"),
    techCheckPopupWindow = document.querySelector(".techCheck-window"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    removeOpenButtons = Array.from(document.querySelectorAll(".removeOpenButton")),
    techCheckOpenButtons = Array.from(document.querySelectorAll(".techCheckOpenButton")),
    techCheckLink = document.querySelector("#techCheck"),
    yearTechCheckLink = document.querySelector("#yearTechCheck"),
    removeConfirmLink = document.querySelector("#removeConfirmLink");


removeOpenButtons.map(function (button) {
   button.addEventListener('click', function () {
       let boatID = button.dataset.id;
       removeConfirmLink.href = "/request/" + boatID + "/remove";

       console.log(removeConfirmLink);

       removePopupWindow.style.display = "flex";
   });
});

techCheckOpenButtons.map(function (button) {
    button.addEventListener('click', function () {
        let boatID = button.dataset.id;
        techCheckLink.href = "/request/" + boatID + "/techCheck";
        yearTechCheckLink.href = "/request/" + boatID + "/yearTechCheck";

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

let removePopupWindow = document.querySelector(".remove-window"),
    techCheckPopupWindow = document.querySelector(".techCheck-window"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    removeOpenButtons = Array.from(document.querySelectorAll(".removeOpenButton")),
    techCheckOpenButtons = Array.from(document.querySelectorAll(".techCheckOpenButton")),
    techCheckLinks = Array.from(document.querySelectorAll(".techCheckLink")),
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
        techCheckLinks.map(function (link) {
            link.href = boatID;
        });

        techCheckPopupWindow.style.display = "flex"
    });
});

closeButtons.map(function (button) {
    button.addEventListener("click", function () {
        removePopupWindow.style.display = "none";
        techCheckPopupWindow.style.display = "none";
    });
});

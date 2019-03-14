let popupWindow = document.querySelector(".popup-window"),
    closeButton = document.querySelector(".closeButton"),
    openButtons = Array.from(document.querySelectorAll(".openButton")),
    removeConfirmLink = document.querySelector("#removeConfirmLink");


openButtons.map(function (button) {
   button.addEventListener('click', function () {
       let boatID = button.dataset.id;
       removeConfirmLink.href = "/request/" + boatID + "/remove";

       console.log(removeConfirmLink);

       popupWindow.style.display = "flex";
   });
});

closeButton.addEventListener("click", function () {
    popupWindow.style.display = "none";
});

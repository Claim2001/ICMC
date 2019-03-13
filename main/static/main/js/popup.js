let popupWindow = document.querySelector(".popup-window"),
    closeButton = document.querySelector(".closeButton"),
    openButtons = Array.from(document.querySelectorAll(".openButton"));


openButtons.map(function (button) {
   button.addEventListener('click', function () {
       popupWindow.style.display = "flex";
   });
});

closeButton.addEventListener("click", function () {
    popupWindow.style.display = "none";
});

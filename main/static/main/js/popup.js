let popupWindow = document.querySelector(".popup-window"),
    closeButton = document.querySelector(".closeButton"),
    openButtons = Array.from(document.querySelectorAll(".openButton"));


openButtons.map(function (button) {
   button.addEventListener('click', function () {
       popupWindow.style.display = "flex";

       setTimeout(function () {
           popupWindow.style.opacity = "1";
       }, 100);
   });
});

closeButton.addEventListener("click", function () {
    // popupWindow.style.display = "none";
    popupWindow.style.opacity = "0";

    setTimeout(function () {
        popupWindow.style.display = "none";
    }, 200);
});

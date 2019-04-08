let showFineButtons = Array.from(document.querySelectorAll(".showFineButton")),
    finePopup = document.querySelector("#finePopup"),
    ownerPopupTitle = document.querySelector(".owner");

showFineButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        console.log(button.dataset.id);
        finePopup.style.display = "block";
        ownerPopupTitle.innerHTML = button.dataset.owner;
    });
});
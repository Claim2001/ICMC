let payButtons = Array.from(document.querySelectorAll(".payButton")),
    payPopup = document.querySelector(".payPopup"),
    closeButtons = Array.from(document.querySelectorAll(".closeButton"));


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
}

payButtons.map(function (button) {
    button.addEventListener("click", function () {
        let id = button.dataset.id;
        document.payForm.action = "request/" + id + "/pay";
        payPopup.style.display = "block";
    });
});
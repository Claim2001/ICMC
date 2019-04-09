let showFineButtons = Array.from(document.querySelectorAll(".showFineButton")),
    finePopup = document.querySelector("#finePopup"),
    ownerPopupTitle = document.querySelector(".owner"),
    reason = document.querySelector(".reason"),
    amount = document.querySelector(".amount"),
    openPayPopupButton = document.querySelector(".openPayPopup"),
    payPopup = document.querySelector(".payPopup"),
    openBankPopupLink = document.querySelector("a#bank"),
    bankPopup = document.querySelector(".bankPopup"),
    fileBox = document.querySelector(".fileBox"),
    fileInput = document.querySelector("input[type='file']"),
    submitButton = document.querySelector("button[type='submit']");

showFineButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        document.payForm.action = button.dataset.id + "/pay/";
        finePopup.style.display = "block";
        ownerPopupTitle.innerHTML = button.dataset.owner;
        reason.innerHTML = button.dataset.reason;
        amount.innerHTML = button.dataset.amount;
    });
});

submitButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    if (isAllowedFileFormat(fileInput.value)) {
        document.payForm.submit();
    } else {
        fileBox.className = "popupBlock fileBox incorrect";
    }
});

openPayPopupButton.addEventListener("click", function () {
    closePopups();
    payPopup.style.display = "block";
});

openBankPopupLink.addEventListener("click", function (evt) {
    evt.preventDefault();

    closePopups();
    bankPopup.style.display = "block";
});

fileBox.addEventListener("click", function () {
    fileInput.click();
});

fileInput.addEventListener("change", function () {
    fileBox.className = isAllowedFileFormat(fileInput.value) ? "popupBlock fileBox filled" : "popupBlock fileBox incorrect";
});

let popupWithCheck = document.querySelector(".popupWithCheck"),
    paymentRequestRows = Array.from(document.querySelectorAll("tr.paymentRequest")),
    closeButtons = Array.from(document.querySelectorAll(".closeButton")),
    checkScanImage = document.querySelector("img.checkScan"),
    checkScanLink = document.querySelector("a.checkScanLink"),
    showAddressPopupLink = document.querySelector("#addressPopupLink"),
    rejectLink = document.querySelector("a#rejectLink"),
    addressPopup = document.querySelector(".addressPopup");


closeButtons.map(function (button) {
    button.addEventListener("click", closePopups);
});

document.addEventListener('keydown', function (evt) {
    if (evt.keyCode === 27) {
        closePopups();
    }
});

function closePopups() {
    popupWithCheck.style.display = "none";
    addressPopup.style.display = "none";
}

showAddressPopupLink.addEventListener("click", function (evt) {
    evt.preventDefault();

    closePopups();
    addressPopup.style.display = "block";
});

paymentRequestRows.map(function (requestRow) {
    requestRow.addEventListener("click", function (evt) {
        evt.preventDefault();

        checkScanLink.href = requestRow.dataset.check;
        document.acceptPaymentForm.action = "/inspector/payments/" + requestRow.dataset.id + "/accept/";
        rejectLink.href = "/inspector/payments/" + requestRow.dataset.id + "/reject/";

        if (checkIfImage(requestRow.dataset.check)) {
            checkScanImage.src = requestRow.dataset.check;
        } else {
            checkScanLink.innerHTML = "просмотр чека"
        }

        popupWithCheck.style.display = "block";
    });
});

function checkIfImage(fileName) {
    fileName = fileName.toLowerCase();

    let parts = fileName.split("."),
        extension = parts[parts.length - 1];

    switch (extension) {
        case "jpg":
        case "png":
        case "jpeg":
        case "bmp":
            return true
    }

    return false;
}

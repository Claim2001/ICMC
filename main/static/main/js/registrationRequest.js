let submitButton = document.querySelector("#submitButton"),
    checkboxes = Array.from(document.querySelectorAll("input[type='checkbox'"));

console.log("This is loaded!");

checkboxes.map(function (checkbox) {
    checkbox.addEventListener('change', function (evt) {
        changeButton(checkboxChecked());
    });
});

function checkboxChecked() {
    let checked = false;

    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checked = true;
            break;
        }
    }

    return checked;
}

function changeButton(isReject) {
    submitButton.className = isReject ? "btn btn-warn" : "btn";
    submitButton.innerText = isReject ? "Отклонить" : "Принять к оплате";
}
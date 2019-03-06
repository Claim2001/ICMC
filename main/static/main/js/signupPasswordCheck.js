let passwordInput = document.querySelector("#id_password"),
    passwordCheckInput = document.querySelector("#passwordCheck"),
    submitButton = document.querySelector("#submitButton"),
    errorMessage = document.querySelector("#clientErrorMessage");

submitButton.addEventListener('click', function (evt) {
    evt.preventDefault();

    // Check if all inputs are filled
    let inputs = Array.from(document.querySelectorAll("input")),
        areInputsFilled = true;

    inputs.map(function (input) {
        if (input.value == "") {
            input.className += " incorrect";

            showErrorMessage("Заполните поля");
            areInputsFilled = false;
        } else {
            input.className = "";
        }
    });

    if (!areInputsFilled) {
        return;
    }

    // check if passwords are no the same
    if (passwordInput.value != passwordCheckInput.value) {
        passwordInput.className += " incorrect";
        passwordCheckInput.className += " incorrect";

        showErrorMessage("Пароли не совпадают");
        return;
    } 

    document.signup.submit();
});

function showErrorMessage(msg) {
    errorMessage.style.display = "block";
    errorMessage.innerHTML = msg;
}
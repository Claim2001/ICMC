let passwordInput = document.querySelector("#id_password"),
    passwordCheckInput = document.querySelector("#passwordCheck"),
    submitButton = document.querySelector("#submitButton"),
    errorMessage = document.querySelector("#clientErrorMessage"),
    emailInput = document.querySelector("#id_email"),
    phoneInput = document.querySelector("#id_phone_number");

submitButton.addEventListener('click', function (evt) {
    evt.preventDefault();

    // Check if all inputs are filled
    let inputs = Array.from(document.querySelectorAll("input")),
        areInputsFilled = true;

    inputs.map(function (input) {
        if (input.value === "") {
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
    if (passwordInput.value !== passwordCheckInput.value) {
        passwordInput.className += " incorrect";
        passwordCheckInput.className += " incorrect";

        console.log("Email is incorrect!");

        showErrorMessage("Пароли не совпадают");
        return;
    }

    // Check if value of phone number input is a real phone number
    // if (!validatePhoneNumber(phoneInput.value)) {
    //     phoneInput.className += " incorrect";
    //     showErrorMessage("Введите корректный номер телефона");
    //     return
    // }

    // check if value of email input is a real email address
    if (!validateEmail(emailInput.value)) {
        emailInput.className += " incorrect";
        showErrorMessage("Введите корректный email-адрес");
        return
    }

    document.signup.submit();
});

function showErrorMessage(msg) {
    errorMessage.style.display = "block";
    errorMessage.innerHTML = msg;
}

function validateEmail(string) {
    let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(string).toLowerCase());
}

// FIXME: doesn't work
function validatePhoneNumber(string) {
    let re = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    return string.match(re);
}


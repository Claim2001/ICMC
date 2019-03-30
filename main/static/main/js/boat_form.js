let pages = Array.from(document.querySelectorAll(".page")),
    steps = Array.from(document.querySelectorAll(".step")),
    nextFormPageButton = document.querySelector("#nextFormPage"),
    prevFormPageButton = document.querySelector("#prevFormPage"),
    submitButton = document.querySelector("#submitButton"),
    errorMessage = document.querySelector("#clientErrorMessage");


nextFormPageButton.addEventListener("click", function () {
    if (checkFieldsFilled() && checkFileFormats()) {
        toggleErrorMessage(false);
        movePage(true);
    } else {
        toggleErrorMessage(true);
    }
});

prevFormPageButton.addEventListener("click", function () {
    movePage(false);
});

submitButton.addEventListener("click", function (evt) {
    evt.preventDefault();

    if (checkFieldsFilled() && checkFileFormats()) {
        toggleErrorMessage(false);
        document.boatForm.submit();
    } else {
        toggleErrorMessage(true);
    }
});

function movePage(isNext) {
    let selectedPage = document.querySelector(".selectedPage"),
        currentStep = document.querySelector(".currentStep"),
        indexOfSelectedPage = pages.indexOf(selectedPage);

    selectedPage.className = "page";
    currentStep.className = "step";

    let nextIndex = isNext ? 1 : -1;
    pages[indexOfSelectedPage + nextIndex].className = "page selectedPage";
    steps[indexOfSelectedPage + nextIndex].className = "step currentStep";
}

function toggleErrorMessage(visible) {
    errorMessage.style.display = visible ? "block" : "none";
}

function checkFieldsFilled() {
    let currentPage = document.querySelector(".selectedPage"),
        inputs = Array.from(currentPage.getElementsByTagName("input"));

    let areFilled = true;

    inputs.map(function (input) {
        if (input.type === "file") {
            let fileBox = input.parentElement.getElementsByClassName("fileBox")[0];
            fileBox.className = input.value === "" || !isAllowedFileFormat(input.value) ? "fileBox incorrect" : "fileBox filled";
        } else {
            input.className = input.value === "" ? "incorrect" : "";
        }

        if (input.value === "") {
            areFilled = false;
        }
    });

    return areFilled;
}

function checkFileFormats() {
    let currentPage = document.querySelector(".selectedPage"),
        fileInputsInCurrentPage = Array.from(currentPage.getElementsByClassName("formFileInput")),
        formatsAreCorrect = true;

    fileInputsInCurrentPage.map(function (fileInput) {
        if (formatsAreCorrect === true) {
            formatsAreCorrect = isAllowedFileFormat(fileInput.value);
        }
    });

    return formatsAreCorrect;
}


let fileBoxes = Array.from(document.querySelectorAll(".fileBox")),
    fileFields = Array.from(document.querySelectorAll("input[type='file']"));


fileBoxes.map(function (box) {
    box.addEventListener("click", function () {
        let fileInput = box.parentElement.getElementsByClassName("formFileInput")[0];
        fileInput.click();
    });
});

fileFields.map(function (field) {
    field.addEventListener("change", function () {
        let fileBox = field.parentElement.getElementsByClassName("fileBox")[0];

        if (!isAllowedFileFormat(field.value)) {
            fileBox.className = "fileBox incorrect";
            toggleErrorMessage(true);

            return
        }

        // if user selected a file then change the class name
        fileBox.className = field.value === "" ? "fileBox" : "fileBox filled";
    })
});

function isAllowedFileFormat(filename) {
    filename = filename.toLowerCase();

    let allowed_extensions = ["jpeg", "png", "jpg", "pdf", "docx", "doc"],
        extension = filename.split('.').pop();

    return allowed_extensions.includes(extension);
}

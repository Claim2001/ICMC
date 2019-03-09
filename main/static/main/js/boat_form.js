let pages = Array.from(document.querySelectorAll(".page")),
    steps = Array.from(document.querySelectorAll(".step")),
    nextFormPageButton = document.querySelector("#nextFormPage"),
    prevFormPageButton = document.querySelector("#prevFormPage");


nextFormPageButton.addEventListener("click", function () {
    movePage(true);
});

prevFormPageButton.addEventListener("click", function() {
    movePage(false);
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


let fileBoxes = Array.from(document.querySelectorAll(".fileBox")),
    fileFields = Array.from(document.querySelectorAll("input"));

fileBoxes.map(function (box) {
    box.addEventListener("click", function () {
        let fileInput = box.parentElement.getElementsByClassName("formFileInput")[0];
        fileInput.click();
    });
});

fileFields.map(function (field) {
    field.addEventListener("change", function () {
        let fileBox = field.parentElement.getElementsByClassName("fileBox")[0];

        // if user selected a file then change the class name
        fileBox.className = field.value === "" ? "fileBox" : "fileBox filled";
    })
})
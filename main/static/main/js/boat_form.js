let pages = Array.from(document.querySelectorAll(".page")),
    nextFormPageButton = document.querySelector("#nextFormPage"),
    prevFormPageButton = document.querySelector("#prevFormPage");


nextFormPageButton.addEventListener("click", function () {
    movePage(true);
});

prevFormPageButton.addEventListener("click", function() {
    movePage(false);
});


function movePage(isNext) {
    var selectedPage = document.querySelector(".selectedPage"),
        indexOfSelectedPage = pages.indexOf(selectedPage);

    selectedPage.className = "page";

    var nextIndex = isNext ? 1 : -1;
    pages[indexOfSelectedPage + nextIndex].className = "page selectedPage";
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
        let className = field.value == "" ? "fileBox" : "fileBox filled";
        fileBox.className = className;
    })
})
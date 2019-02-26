var pages = Array.from(document.querySelectorAll(".page")),
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
let boatRows = Array.from(document.querySelectorAll(".boatRow")),
    addFinePopup = document.querySelector("#addFinePopup"),
    fullNamePopupTitle = document.querySelector(".fullNameTitle");

boatRows.map(function (row) {
   row.addEventListener("click", function () {
       document.fineForm.action = row.dataset.id;
       fullNamePopupTitle.innerHTML = row.dataset.owner;

       addFinePopup.style.display = "block";
   });
});

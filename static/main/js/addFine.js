let boatRows = Array.from(document.querySelectorAll(".boatRow")),
    addFinePopup = document.querySelector("#addFinePopup"),
    fullNamePopupTitle = document.querySelector(".fullNameTitle"),
    boatIDInput = document.querySelector(".boatID");

boatRows.map(function (row) {
   row.addEventListener("click", function () {
       boatIDInput.value = row.dataset.id;
       fullNamePopupTitle.innerHTML = row.dataset.owner;

       addFinePopup.style.display = "block";
   });
});

let selectAllCheckbox = document.querySelector("#selectAll"),
    requestCheckboxes = Array.from(document.querySelectorAll("input.requestCheckbox"));


selectAllCheckbox.addEventListener("change", function () {
    requestCheckboxes.map(function (checkbox) {
        checkbox.checked = selectAllCheckbox.checked;
    });
});

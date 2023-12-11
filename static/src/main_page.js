// JavaScript source code

// Function to show a form section
function showFormSection(sectionId) {
    const sections = document.querySelectorAll('#main-content section');
    sections.forEach(section => {
        section.style.display = 'none'; // Hide all sections
    });
    const formSection = document.querySelector(`#${sectionId}`);
    formSection.style.display = 'block'; // Show the selected section
}

document.querySelectorAll('#create-new a').forEach(anchor => {
    anchor.addEventListener('click', function (event) {
        event.preventDefault();
        const sectionId = this.getAttribute('href').substring(1);
        showFormSection(sectionId);
    });
});

function loadFileList() {
}

document.addEventListener('DOMContentLoaded', function () {
    loadFileList();
});

function submitCaseForm() {
    const caseForm = document.getElementById('case-form');
    caseForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(caseForm);
        console.log('Form Data Submitted: ', Object.fromEntries(formData.entries()));
    });
}

document.getElementById('case-form').addEventListener('submit', submitCaseForm);

function menuShow() {
    let item = document.getElementById("left-menu");
    if (item.style.left === "0px") {
        item.style.left = "-10em"
        item.style.opacity = "0"
    } else {
        item.style.left = "0px"
        item.style.opacity = "1"
    }
}
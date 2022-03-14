const nameField = document.getElementById("name");
const email = document.getElementById("email");
const subject = document.getElementById("subject");
const message = document.getElementById("message");


nameField.addEventListener("input", function (event) {
    if (nameField.value.length > 4 && nameField.value.length < 256) {
        changeBorder(nameField, 'green');
    }
    else {
        changeBorder(nameField, 'red');
    }
});

email.addEventListener("input", function (event) {
    if (email.value.length > 4 && email.value.length < 256) {
        changeBorder(email, 'green');
    }
    else {
        changeBorder(email, 'red');
    }
});

subject.addEventListener("input", function (event) {
    if (subject.value.length > 4 && subject.value.length < 256) {
        changeBorder(subject, 'green');
    }
    else {
        changeBorder(subject, 'red');
    }
});

message.addEventListener("input", function (event) {
    if (message.value.length > 4 && message.value.length < 2001) {
        changeBorder(message, 'green');
    }
    else {
        changeBorder(message, 'red');
    }
});


function changeBorder(container, color) {
    container.style.borderColor = color;
};
// Question 1: The Dirty Code
const yes = document.querySelector('#yes');
const test = document.createElement('p');
document.querySelector('#yes').addEventListener('click', function () {
    yes.style.backgroundColor = 'red';
    test.textContent = 'Incorrect!';
});
const no = document.querySelector('#no');
document.querySelector('#no').addEventListener('click', function () {
    no.style.backgroundColor = 'red';
    test.textContent = 'Incorrect!';
});
const question = document.querySelector('#question');
document.querySelector('#question').addEventListener('click', function () {
    question.style.backgroundColor = 'green';
    test.textContent = 'Correct!';
});
const what = document.querySelector('#what');
document.querySelector('#what').addEventListener('click', function () {
    what.style.backgroundColor = 'red';
    test.textContent = 'Incorrect!';
});
// Question 1: The Better Way


// Question 2: The Dirty Code

// Declaring Variables
const answer = document.querySelector('#q2.q2').value;
const field = document.querySelector('#q2');
const submit = document.querySelector('.submit');

// Checking after submitting
document.querySelector('.submit').addEventListener('click', function () {
    const para = document.createElement('p');
    if (answer === '...') {
        field.style.backgroundColor = 'green';
        para.textContent = 'Correct!';
    }
    else {
        field.style.backgroundColor = 'red';
        para.textContent = 'Incorrect!';
    }
    document.body.appendChild(para);
});



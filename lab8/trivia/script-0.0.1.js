// Question 1: The Dirty Code
/*
const test = document.createElement('p');

const yes = document.querySelector('#yes');
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
*/

// Question 1: The Better Way
/*
const answerQ1 = document.querySelector('.q1');
const q1Text = document.querySelector('#q1Text');

answerQ1.addEventListener('click', function () {
    if (answerQ1.value === 'There is no question') {
        answerQ1.style.backgroundColor = 'green';
        q1Text.textContent = 'Correct!';
    } else {
        answerQ1.style.backgroundColor = 'red';
        q1Text.textContent = 'Incorrect!';
    }
});
*/

const buttons = document.querySelectorAll('.q1')
const q1Text = document.querySelector('#q1Text');

buttons.forEach((btn) => {
    btn.addEventListener("click", (event) => {
        if (btn.value === 'question') {
            btn.style.backgroundColor = 'green';
            q1Text.textContent = 'Correct!';
        } else {
            btn.style.backgroundColor = 'red';
            q1Text.textContent = 'Incorrect!';
        }
    });
});


// Question 2: The Dirty Code

// Declaring Variables
const answer = document.querySelector('.q2');
const field = document.querySelector('#q2');
const submit = document.querySelector('.submit');
const q2Text = document.querySelector('#q2Text');

// Checking after submitting
document.querySelector('.submit').addEventListener('click', function () {
    if (answer.value === 'There is no question') {
        field.style.backgroundColor = 'green';
        q2Text.textContent = 'Correct!';
    } else {
        field.style.backgroundColor = 'red';
        q2Text.textContent = 'Incorrect!';
    }
});



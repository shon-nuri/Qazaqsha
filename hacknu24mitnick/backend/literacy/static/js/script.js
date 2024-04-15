// Add event listener to the form submission
document.getElementById('grammarForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent form submission

    // Get the user's chosen answer
    const selectedAnswer = document.querySelector('input[name="verb"]:checked');
    
    // Define the correct answer
    const correctAnswer = 'runs';

    // Get the element to display the result
    const resultElement = document.getElementById('result');

    // Check if the user's answer matches the correct answer
    if (selectedAnswer && selectedAnswer.value === correctAnswer) {
        // Display success message if the answer is correct
        resultElement.textContent = 'Correct! Well done!';
        resultElement.style.color = 'green';
    } else {
        // Display failure message if the answer is incorrect
        resultElement.textContent = 'Incorrect. Try again!';
        resultElement.style.color = 'red';
    }
});

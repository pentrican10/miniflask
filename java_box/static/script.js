document.addEventListener('DOMContentLoaded', function () {
  const userInput = document.getElementById('user_input');
  const displayArea = document.getElementById('display_area');
  let enteredText = ''; // Variable to store user input

  userInput.addEventListener('input', function () {
    enteredText = userInput.value; // Update the enteredText variable as the user types
  });

  function resizeDisplayArea() {
    displayArea.style.height = userInput.scrollHeight + 'px';
  }

  userInput.addEventListener('input', resizeDisplayArea);

  window.addEventListener('resize', resizeDisplayArea);

  // Function to display the text when the "GO" button is clicked
  function displayText() {
    displayArea.innerHTML = `${enteredText}`;
  }

  // Attach the displayText function to the "GO" button click event
  const goButton = document.getElementById('go_button');
  goButton.addEventListener('click', displayText);
});

// Initialize the output box
const outputBox = document.getElementById('outputBox');

// Initialize the input field
const userInput = document.getElementById('messageInput');

// Initialize the send button
const sendButton = document.querySelector('.send-button');

// Function to handle sending the user input
function sendMessage() {
  // Get the user input value
  const userText = userInput.value.trim();

  if (userText) {
    // Clear the output box before each new message
    outputBox.innerHTML = '';

    //TODO Send the request to your API or backend to process the user's input and generate a response
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userText }),
    })
    .then((res) => res.json())
    .then((data) => {
      // Update the output box with the response
      const message = document.createElement('p');
      message.textContent = data.response;
      outputBox.appendChild(message);
      
      // Clear the input field after each new message
      userInput.value = '';
    });
  }
}

// Event listener for the "Enter" key press
userInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// Event listener for the "Send" button click
sendButton.addEventListener('click', sendMessage);

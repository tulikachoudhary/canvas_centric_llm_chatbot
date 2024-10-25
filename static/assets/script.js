document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const outputBox = document.getElementById('outputBox');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        // Append the new message to the output box
        const messageElement = document.createElement('div');
        messageElement.innerText = data.message; // Set the response message
        outputBox.appendChild(messageElement); // Append the message
    });
});

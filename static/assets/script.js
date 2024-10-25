function scrollToBottom() {
    const outputBox = document.getElementById('outputBox');
    outputBox.scrollTop = outputBox.scrollHeight; // Scroll to the bottom
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        
        // Append new text to outputBox
        const outputBox = document.getElementById('outputBox');
        outputBox.innerText += `\n${data.message}`;  // Append without clearing the previous content
        
        // Automatically scroll to the bottom
        scrollToBottom();
    });
});


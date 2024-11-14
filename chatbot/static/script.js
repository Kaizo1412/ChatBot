// Add this function to handle sending messages
function sendMessage() {
    var userInput = document.getElementById('chat-input').value;

    // Check if the input is not empty
    if (userInput.trim() !== '') {
        // Send user input to the server using fetch
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'user_input=' + encodeURIComponent(userInput),
        })
        .then(response => response.json())
        .then(data => {
            // Update the chat container with the server's response
            var chatContainer = document.querySelector('.chat-container');
            var newChatMessage = document.createElement('div');
            newChatMessage.innerHTML = 'User: ' + userInput + '<br> M.A.R.V.I.S: ' + data.response; 
            chatContainer.appendChild(newChatMessage);

            // Clear the input field after sending the message
            document.getElementById('chat-input').value = '';
        });

    }
}



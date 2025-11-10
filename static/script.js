const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", async () => {
    const message = userInput.value;
    if (!message) return;

    appendMessage("You", message);
    userInput.value = "";

    appendMessage("Bot", "Typing...");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        updateLastBotMessage(data.reply);
    } catch (err) {
        updateLastBotMessage("Error connecting to server.");
    }
});

function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function updateLastBotMessage(text) {
    const messages = chatBox.getElementsByClassName("message");
    messages[messages.length - 1].innerHTML = `<strong>Bot:</strong> ${text}`;
}

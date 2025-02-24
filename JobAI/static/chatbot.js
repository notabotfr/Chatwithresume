document.addEventListener("DOMContentLoaded", function() {
    const chatbotToggle = document.getElementById("chatbot-toggle");
    const chatbotContainer = document.getElementById("chatbot-container");
    const closeChatbot = document.getElementById("close-chatbot");
    chatbotToggle.addEventListener("click", function() {
        chatbotContainer.style.display = chatbotContainer.style.display === "block" ? "none" : "block";
    });
    closeChatbot.addEventListener("click", function() {
        chatbotContainer.style.display = "none";
    });
});
async function sendMessage() {
    let inputField = document.getElementById("userInput");
    let chatbox = document.getElementById("chatbox");
    let userMessage = inputField.value.trim();
   
    if (userMessage === "") return; // Prevent empty messages
    // Display user message
    chatbox.innerHTML += <p><b>You:</b> ${userMessage}</p>;
    inputField.value = ""; // Clear input field
    try {
        let response = await fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ model: "qwen2.5", prompt: userMessage }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        let fullResponse = "";
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            let chunk = decoder.decode(value, { stream: true });
            try {
                let jsonChunk = JSON.parse(chunk);
                if (jsonChunk.response) {
                    fullResponse += jsonChunk.response; // Append response
                }
            } catch (err) {
                console.error("JSON parsing error:", err);
            }
        }
        // Display final bot response
        chatbox.innerHTML += <p><b>Bot:</b> ${fullResponse}</p>;
       
        // Auto-scroll to the latest message
        chatbox.scrollTop = chatbox.scrollHeight;
    } catch (error) {
        console.error("Error:", error);
        chatbox.innerHTML += <p><b>Bot:</b> Sorry, I couldn't process your request.</p>;
    }
}
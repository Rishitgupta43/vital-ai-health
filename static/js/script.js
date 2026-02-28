const form = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const clearBtn = document.querySelector(".clear-btn");

/* SEND MESSAGE */
form.addEventListener("submit", async function(e) {
    e.preventDefault();

    const msg1 = document.getElementById("message1").value.trim();
    const msg2 = document.getElementById("message2").value.trim();
    const msg3 = document.getElementById("message3").value.trim();

    if (!msg1) return;

    if (!chatBox.classList.contains("active")) {
        chatBox.classList.add("active");
    }

    addMessage("You", msg1, "user");

    const formData = new FormData();
    formData.append("message1", msg1);
    formData.append("message2", msg2);
    formData.append("message3", msg3);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            body: formData
        });

        const data = await response.text();
        addMessage("V.I.T.A.L", data, "ai");

    } catch (error) {
        addMessage("System", "⚠️ Server error. Please try again.", "ai");
    }

    form.reset();
});

/* ADD MESSAGE */
function addMessage(sender, text, type) {

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", type);

    messageDiv.innerHTML = `
        <strong>${sender}</strong><br><br>
        ${text.replace(/\n/g, "<br>")}
    `;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* CLEAR CHAT */
clearBtn.addEventListener("click", function() {

    const messages = document.querySelectorAll(".message");

    if (messages.length === 0) return;

    messages.forEach(msg => {
        msg.classList.add("fade-out");
    });

    setTimeout(() => {
        chatBox.innerHTML = "";
        chatBox.classList.remove("active");
    }, 500);

});
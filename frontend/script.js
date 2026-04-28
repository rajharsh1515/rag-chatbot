const BASE_URL = "http://127.0.0.1:8000";

// Upload PDF
document.getElementById("uploadForm").onsubmit = async (e) => {
    e.preventDefault();

    let formData = new FormData(e.target);

    let res = await fetch(`${BASE_URL}/upload`, {
        method: "POST",
        body: formData
    });

    let data = await res.json();
    document.getElementById("uploadStatus").innerText = data.message || data.error;
};

// Ask Question
async function ask() {
    let question = document.getElementById("question").value;

    if (!question) return;

    // Show question
    let chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<p class="user">You: ${question}</p>`;

    let res = await fetch(`${BASE_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    let data = await res.json();

    // Show answer
    chatBox.innerHTML += `<p class="bot">Bot: ${data.answer}</p>`;

    document.getElementById("question").value = "";
}
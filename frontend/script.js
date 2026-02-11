const messages = document.getElementById("messages");
const input = document.getElementById("input");

function addMessage(text, cls) {
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

async function send() {
  const text = input.value.trim();
  if (!text) return;

  addMessage("Você: " + text, "user");
  input.value = "";

  addMessage("🤖 Pensando...", "bot");

  const res = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: text})
  });

  const data = await res.json();
  messages.lastChild.textContent = "🤖 " + data.answer;
}

input.addEventListener("keydown", e => {
  if (e.key === "Enter") send();
});

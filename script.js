const input = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const chat = document.querySelector(".chat-container");

function addMessage(text, sender = "user") {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = sender === "user" ? "🧑" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = `<p>${text}</p>`;

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chat.appendChild(msg);

  chat.scrollTop = chat.scrollHeight;
}

function fakeBotReply(userText) {
  setTimeout(() => {
    addMessage("Entendi! Em breve vou processar isso 🤖✨", "bot");
  }, 600);
}

sendBtn.addEventListener("click", () => {
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  fakeBotReply(text);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendBtn.click();
});

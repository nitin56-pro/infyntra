function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  const userMessage = input.value;
  if (!userMessage) return;

  chatBox.innerHTML += `<p><strong>You:</strong> ${userMessage}</p>`;
  input.value = "";

  fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: userMessage})
  })
  .then(res => res.json())
  .then(data => {
    chatBox.innerHTML += `<p><strong>Infyntra:</strong> ${data.answer}</p>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  });
}

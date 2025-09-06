async function ask() {
  const q = document.getElementById("question").value;
  const outputBox = document.getElementById("output");
  const loading = document.getElementById("loading");

  if (!q.trim()) return;

  // Show loading
  loading.style.display = "block";
  outputBox.textContent = "";  // Clear previous output

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question: q})
    });
    const data = await res.json();

    // Hide loading
    loading.style.display = "none";

    // Show AI response
    outputBox.textContent = data.response;
  } catch (err) {
    loading.style.display = "none";
    outputBox.textContent = "Error: " + err.message;
  }
}

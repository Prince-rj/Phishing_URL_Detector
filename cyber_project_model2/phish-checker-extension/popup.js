async function getCurrentTabUrl() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab.url;
}

function showNotification(title, message, isGood) {
  chrome.runtime.sendMessage({
    type: "showNotification",
    title: title,
    message: message,
    isGood: isGood
  });
}

getCurrentTabUrl().then(url => {
  document.getElementById("url").textContent = url;

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url })
  })
  .then(response => response.json())
  .then(data => {
    const prediction = data.prediction;
    const resultEl = document.getElementById("result");

    if (prediction === "bad") {
      resultEl.textContent = "Phishing or Bad Site";
      resultEl.className = "bad";
      showNotification("Alert", "This site might be phishing!", false);
    } else {
      resultEl.textContent = "✅ Legit or Safe Site";
      resultEl.className = "good";
      showNotification("✅ Safe", "This site appears legit.", true);
    }
  })
  .catch(err => {
    document.getElementById("result").textContent = "⚠️ Error connecting to model server";
    console.error(err);
  });
});

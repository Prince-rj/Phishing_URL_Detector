chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "url": message.url })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Prediction:", data.result);
    });
});

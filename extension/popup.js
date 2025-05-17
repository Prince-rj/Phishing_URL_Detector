document.getElementById("check").addEventListener("click", () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        let url = tabs[0].url;
        fetch("http://127.0.0.1:5000/predict", {  // Calls local Flask API
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "url": url })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerText = data.result;
        });
    });
});

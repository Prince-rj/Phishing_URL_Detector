chrome.webNavigation.onCompleted.addListener(async (details) => {
  const tabId = details.tabId;

  chrome.tabs.get(tabId, async (tab) => {
    if (!tab.url.startsWith("http")) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: tab.url })
      });

      const data = await response.json();
      const prediction = data.prediction;
      console.log(prediction)

      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: prediction === "bad" ? "🚨 Phishing Alert" : "✅ Safe Site",
        message: prediction === "bad"
          ? "This site might be malicious. Stay alert!"
          : "This site appears legit.",
        priority: 2
      }, (notificationId) => {
        setTimeout(() => chrome.notifications.clear(notificationId), 3000);
      });


    } catch (error) {
      console.error("Background check failed:", error);
    }
  });
}, {
  url: [{ schemes: ["http", "https"] }]
});

from flask import Flask, request, jsonify
import joblib
import tldextract
import re
import pandas as pd

app = Flask(__name__)
model = joblib.load("C:\\Users\\KIIT\\Desktop\\cyberProject\\ML model\\phishing_model3.pkl")

# Feature extraction (same as training)
def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_ip'] = 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0
    features['has_at'] = 1 if "@" in url else 0
    features['has_hyphen'] = 1 if "-" in url else 0
    features['has_https'] = 1 if "https" in url else 0
    features['num_subdirs'] = url.count('/')
    domain_info = tldextract.extract(url)
    features['domain_length'] = len(domain_info.domain)
    features['is_suspicious_tld'] = 1 if domain_info.suffix in ["tk", "ml", "ga", "cf", "gq"] else 0
    return features

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    features = extract_features(url)
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    
    result = "phishing" if prediction == 1 else "legitimate"
    return jsonify({'url': url, 'prediction': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

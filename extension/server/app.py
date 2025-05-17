from flask import Flask, request, jsonify
import pickle
import pandas as pd
from model.predict import extract_features

app = Flask(__name__)

# Load Model
model = pickle.load(open("model/phishing_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]
    features = extract_features(url)
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    result = "Phishing" if prediction == 1 else "Legit"
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)

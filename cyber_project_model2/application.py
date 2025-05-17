from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load the model and vectorizer
with open("phishing_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

@app.route("/", methods=["GET"])
def home():
    return "Phishing Detection API is running."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "")
    print(url)

    # Transform the URL using the vectorizer
    features = vectorizer.transform([url])

    # Predict using the model
    prediction = model.predict(features)
    print(prediction)
    result = "bad" if prediction[0] == 1 else "✅ Legitimate"
    print(result)
    return jsonify({"prediction": result})

if __name__ == "__main__":
    app.run(debug=True)

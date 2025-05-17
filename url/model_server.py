# from flask import Flask, request, jsonify
# import pickle

# app = Flask(__name__)

# with open("phishing.pkl", "rb") as f:
#     model = pickle.load(f)

# @app.route("/", methods=["GET"])
# def home():
#     return "Phishing Detection API is running."

# @app.route("/favicon.ico")
# def favicon():
#     return '', 204

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.get_json()
#     url = data.get("url", "")
#     prediction = model.predict([url])[0]
#     return jsonify({"prediction": prediction})

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS  # 👈 Add this
import pickle

app = Flask(__name__)
CORS(app)  # 👈 Add this line to allow cross-origin requests

with open("phishing.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return "Phishing Detection API is running."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "")
    prediction = model.predict([url])[0]
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)

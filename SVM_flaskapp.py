import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
from flask import Flask, request, jsonify

# Step 1: Load and preprocess the dataset
# Load the dataset
df = pd.read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')

# Select features that can be extracted from the URL
# For demonstration, let's use 'URLLength', 'NoOfSubDomain', 'IsHTTPS', and 'TLDLength'
# Ensure these features are available in your dataset
features = ['URLLength', 'NoOfSubDomain', 'IsHTTPS', 'TLDLength']
X = df[features]
y = df['label']  # Assuming 'label' is the target column with 0 for legitimate and 1 for phishing

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Train the SVM classifier
svm_classifier = SVC(kernel='linear', random_state=42)
svm_classifier.fit(X_train, y_train)

# Evaluate the model
y_pred_svm = svm_classifier.predict(X_test)
accuracy_svm = accuracy_score(y_test, y_pred_svm)
print("SVM Accuracy:", accuracy_svm)
print("SVM Classification Report:")
print(classification_report(y_test, y_pred_svm, digits=4))

# Save the trained model
joblib.dump(svm_classifier, 'svm_model.pkl')

# Step 3: Create a Flask API for the model
app = Flask(__name__)

# Load the trained model
model = joblib.load('svm_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url_features = extract_features(data['url'])  # Implement this function based on your feature selection
    features_df = pd.DataFrame([url_features], columns=features)
    prediction = model.predict(features_df)[0]
    return jsonify({'prediction': int(prediction)})

if __name__ == '__main__':
    app.run(debug=True)

# Note: Implement the 'extract_features' function to extract the necessary features from the URL string.

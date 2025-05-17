# 🔐 Phishing Website Detection using URL Analysis and Machine Learning

This project presents a lightweight, real-time phishing URL detection system powered by machine learning and integrated into a Google Chrome extension.

## 📌 Executive Summary

Phishing websites trick users into revealing personal information by mimicking legitimate sites. Traditional detection methods are often slow and resource-heavy. Our solution analyzes only the URL, using machine learning models to detect phishing attempts efficiently and accurately—then delivers real-time alerts via a browser extension.

## 🎯 Objectives

- Detect phishing websites using URL-based features.
- Build a Chrome extension to alert users in real-time.
- Ensure fast, lightweight, and user-friendly phishing detection.

## 🧠 Machine Learning Models

The project evaluates multiple models:
- **XGBoost**
- **Logistic Regression**
- **Bernoulli Naive Bayes (BernoulliNB)**
- **Support Vector Machines (SVM)**
- **Random Forest**
- **TF-IDF Vectorization + Logistic Regression**

### 📈 Best Results
- **TF-IDF + Logistic Regression**: 99.67% accuracy
- **BernoulliNB**: 99.6% accuracy
- **XGBoost**: 99% accuracy

## 🛠️ Features Extracted

From each URL:
- URL length
- Presence of HTTPS
- Number of digits, hyphens, dots, slashes
- IP-based domain detection
- Homograph similarity (e.g., `google.com`)
- Punycode detection
- Zero-width character detection

## 🔗 Chrome Extension

The trained ML model is integrated into a Chrome extension that:
- Analyzes the current URL
- Flags phishing attempts in real-time
- Displays user alerts without loading the full webpage

## 🧪 Methodology

1. URL dataset collection (legitimate + phishing)
2. Feature extraction from raw URLs
3. Model training and evaluation
4. Model export via `pickle`
5. Chrome Extension development (HTML, JS, JSON)
6. Real-time phishing alert deployment

## 🧰 Tech Stack

- **Python** (scikit-learn, XGBoost, pandas, numpy)
- **VS Code** for development
- **GitHub** for version control
- **Google Chrome APIs** for extension development

## 📚 References

- Jain, A., Gupta, B. (2018). *URL-based Phishing Detection*
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions/)

## 👨‍💻 Team Members

- **Jatin Mudiraj** – Logistic Regression, Chrome Extension
- **Prince Raj** – BernoulliNB + Integration
- **Shubham Jha** – XGBoost Modeling, Extension UI

## 🔮 Future Work

- Integrate Google Safe Browsing API
- Expand dataset with multi-language URLs
- Explore deep learning for generalization

---


## STEPS TO RUN


Step1: To run the different models and applications first we need to go to the extension folder of the project and upload this to a browser

Step2: After uploading this file we need to come back to this folder and then we need to run the backend for all the models
BernauliNB: python bernaulinb_flaskapp.py
SVM: python SVM_flaskapp.py
TFID and Logistic Regression: python TFID_and_Logistic_regression_flaskapplication.py
XGBoost: python XGBoost_flask_app.py


Step 3: Go to browser and see the model working.

## Summary

All these models are using the pickle file which has been trained and then we convert the weights in pickle file and then using these files we are gettting the prediction for each of the urls.

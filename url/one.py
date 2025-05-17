import numpy as np
import pandas as pd
import warnings
import pickle

from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

warnings.filterwarnings('ignore')

def load_and_process_data(csv_path):
    # Load dataset
    phish_data = pd.read_csv(csv_path)
    
    # Tokenization
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    phish_data['text_tokenized'] = phish_data.URL.map(lambda t: tokenizer.tokenize(t))
    
    # Stemming
    stemmer = SnowballStemmer("english")
    phish_data['text_stemmed'] = phish_data['text_tokenized'].map(lambda l: [stemmer.stem(word) for word in l])
    
    # Join the words to form sentences
    phish_data['text_sent'] = phish_data['text_stemmed'].map(lambda l: ' '.join(l))
    
    return phish_data

def train_model(phish_data):
    trainX, testX, trainY, testY = train_test_split(phish_data.URL, phish_data.Label)

    pipeline = make_pipeline(
        CountVectorizer(tokenizer=RegexpTokenizer(r'[A-Za-z]+').tokenize, stop_words='english'),
        LogisticRegression()
    )
    
    pipeline.fit(trainX, trainY)
    
    print("Training Accuracy:", round(pipeline.score(trainX, trainY), 4))
    print("Testing Accuracy:", round(pipeline.score(testX, testY), 4))
    
    # Save model
    with open("phishing.pkl", "wb") as f:
        pickle.dump(pipeline, f)
    
    print("Model saved as phishing.pkl")
    return pipeline

def predict_url(url, model_path='phishing.pkl'):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([url])
    
    if prediction[0] == 'bad':
        print(f"The URL '{url}' is: 🚨 Phishing or Bad")
    else:
        print(f"The URL '{url}' is: ✅ Legit or Good")

if __name__ == "__main__":
    # Step 1: Load and process data
    data_path = "phishing_site_urls/phishing_site_urls.csv"  # Change if needed
    phish_data = load_and_process_data(data_path)
    
    # Step 2: Train and save model
    train_model(phish_data)
    
    # Step 3: Predict new URLs
    urls_to_test = [
        "http://example.com",
        "www.google.com/search?q=phishing+site+urls+kaggle",
        "google.com",
        "www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php",
        "https://cpplan.online"
    ]
    
    print("\n--- URL Predictions ---")
    for url in urls_to_test:
        predict_url(url)
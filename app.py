from flask import Flask, request, jsonify
import joblib
import tldextract
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd




app = Flask(__name__)
model = joblib.load("svm_phishing_model.pkl")  # Replace with your .pkl file path
expected_cols = ['URLLength', 'DomainLength', 'IsDomainIP', 'TLD', 'URLSimilarityIndex',
                 'CharContinuationRate', 'TLDLegitimateProb', 'URLCharProb', 'TLDLength',
                 'NoOfSubDomain', 'HasObfuscation', 'NoOfObfuscatedChar',
                 'ObfuscationRatio', 'NoOfLettersInURL', 'LetterRatioInURL',
                 'NoOfDegitsInURL', 'DegitRatioInURL', 'NoOfEqualsInURL',
                 'NoOfQMarkInURL', 'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL',
                 'SpacialCharRatioInURL', 'IsHTTPS', 'LineOfCode', 'LargestLineLength',
                 'HasTitle', 'DomainTitleMatchScore', 'URLTitleMatchScore', 'HasFavicon',
                 'Robots', 'IsResponsive', 'NoOfURLRedirect', 'NoOfSelfRedirect',
                 'HasDescription', 'NoOfPopup', 'NoOfiFrame', 'HasExternalFormSubmit',
                 'HasSocialNet', 'HasSubmitButton', 'HasHiddenFields',
                 'HasPasswordField', 'Bank', 'Pay', 'Crypto', 'HasCopyrightInfo',
                 'NoOfImage', 'NoOfCSS', 'NoOfJS', 'NoOfSelfRef', 'NoOfEmptyRef',
                 'NoOfExternalRef']

# def extract_features(url):
#     parsed_url = urlparse(url)
#     ext = tldextract.extract(url)

#     try:
#         domain = ext.domain
#         suffix = ext.suffix
#         subdomain = ext.subdomain
#     except:
#         domain, suffix, subdomain = "", "", ""

#     features = {
#         'URLLength': len(url),
#         'DomainLength': len(domain),
#         'IsDomainIP': 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0,
#         'TLD': hash(suffix) % 1000 if suffix else 0,
#         'URLSimilarityIndex': 0,
#         'CharContinuationRate': 0,
#         'TLDLegitimateProb': 0,
#         'URLCharProb': 0,
#         'TLDLength': len(suffix),
#         'NoOfSubDomain': len(subdomain.split('.')) if subdomain else 0,
#         'HasObfuscation': 0,
#         'NoOfObfuscatedChar': 0,
#         'ObfuscationRatio': 0,
#         'NoOfLettersInURL': sum(c.isalpha() for c in url),
#         'LetterRatioInURL': sum(c.isalpha() for c in url) / len(url),
#         'NoOfDegitsInURL': sum(c.isdigit() for c in url),
#         'DegitRatioInURL': sum(c.isdigit() for c in url) / len(url),
#         'NoOfEqualsInURL': url.count('='),
#         'NoOfQMarkInURL': url.count('?'),
#         'NoOfAmpersandInURL': url.count('&'),
#         'NoOfOtherSpecialCharsInURL': sum(1 for c in url if not c.isalnum() and c not in ['/', ':', '.', '?', '=', '&']),
#         'SpacialCharRatioInURL': sum(1 for c in url if not c.isalnum()) / len(url),
#         'IsHTTPS': 1 if parsed_url.scheme == 'https' else 0,
#         'LineOfCode': 0,
#         'LargestLineLength': 0,
#         'HasTitle': 0,
#         'DomainTitleMatchScore': 0,
#         'URLTitleMatchScore': 0,
#         'HasFavicon': 0,
#         'Robots': 0,
#         'IsResponsive': 0,
#         'NoOfURLRedirect': 0,
#         'NoOfSelfRedirect': 0,
#         'HasDescription': 0,
#         'NoOfPopup': 0,
#         'NoOfiFrame': 0,
#         'HasExternalFormSubmit': 0,
#         'HasSocialNet': 0,
#         'HasSubmitButton': 0,
#         'HasHiddenFields': 0,
#         'HasPasswordField': 0,
#         'Bank': int("bank" in url.lower()),
#         'Pay': int("pay" in url.lower()),
#         'Crypto': int("crypto" in url.lower() or "btc" in url.lower()),
#         'HasCopyrightInfo': 0,
#         'NoOfImage': 0,
#         'NoOfCSS': 0,
#         'NoOfJS': 0,
#         'NoOfSelfRef': 0,
#         'NoOfEmptyRef': 0,
#         'NoOfExternalRef': 0
#     }

#     # Finalize in expected order
#     final_features = [features.get(feat, 0) for feat in expected_cols]
#     return final_features



def extract_url_base_features(url):
    parsed_url = urlparse(url)
    ext = tldextract.extract(url)
    domain = ext.domain
    suffix = ext.suffix
    subdomain = ext.subdomain

    features = {
        'URLLength': len(url),
        'DomainLength': len(domain),
        'IsDomainIP': 1 if re.match(r'\d+\.\d+\.\d+\.\d+', ext.registered_domain) else 0,
        'TLD': hash(suffix) % 1000 if suffix else 0,
        'TLDLength': len(suffix),
        'NoOfSubDomain': len(subdomain.split('.')) if subdomain else 0,
        'Bank': int("bank" in url.lower()),
        'Pay': int("pay" in url.lower()),
        'Crypto': int("crypto" in url.lower() or "btc" in url.lower()),
        'IsHTTPS': 1 if parsed_url.scheme == 'https' else 0,
    }
    return features, parsed_url, domain, suffix, subdomain

def extract_char_features(url):
    features = {
        'NoOfLettersInURL': sum(c.isalpha() for c in url),
        'LetterRatioInURL': sum(c.isalpha() for c in url) / len(url),
        'NoOfDegitsInURL': sum(c.isdigit() for c in url),
        'DegitRatioInURL': sum(c.isdigit() for c in url) / len(url),
        'NoOfEqualsInURL': url.count('='),
        'NoOfQMarkInURL': url.count('?'),
        'NoOfAmpersandInURL': url.count('&'),
        'NoOfOtherSpecialCharsInURL': sum(1 for c in url if not c.isalnum() and c not in ['/', ':', '.', '?', '=', '&']),
        'SpacialCharRatioInURL': sum(1 for c in url if not c.isalnum()) / len(url),
    }
    return features

def extract_html_features(url):
    try:
        response = requests.get(url, timeout=5)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        lines = html.splitlines()
        line_lengths = [len(line) for line in lines]

        title = soup.title.string.lower() if soup.title and soup.title.string else ""

        features = {
            'LineOfCode': len(lines),
            'LargestLineLength': max(line_lengths) if line_lengths else 0,
            'HasTitle': 1 if title else 0,
            'DomainTitleMatchScore': int(any(word in title for word in urlparse(url).netloc.split('.'))),
            'URLTitleMatchScore': int(any(word in title for word in url.split('/'))),
            'HasFavicon': 1 if soup.find("link", rel=lambda x: x and "icon" in x.lower()) else 0,
            'Robots': 1 if '/robots.txt' in html.lower() else 0,
            'IsResponsive': 1 if 'viewport' in html.lower() else 0,
            'NoOfURLRedirect': html.lower().count("http-equiv") + html.lower().count("window.location"),
            'NoOfSelfRedirect': html.lower().count("window.location.href"),
            'HasDescription': 1 if soup.find("meta", attrs={"name": "description"}) else 0,
            'NoOfPopup': html.lower().count("window.open"),
            'NoOfiFrame': len(soup.find_all('iframe')),
            'HasExternalFormSubmit': 1 if any('action="http' in str(form) for form in soup.find_all('form')) else 0,
            'HasSocialNet': 1 if any(sn in html.lower() for sn in ['facebook', 'twitter', 'linkedin']) else 0,
            'HasSubmitButton': 1 if soup.find('input', {'type': 'submit'}) else 0,
            'HasHiddenFields': 1 if soup.find('input', {'type': 'hidden'}) else 0,
            'HasPasswordField': 1 if soup.find('input', {'type': 'password'}) else 0,
            'HasCopyrightInfo': 1 if "©" in html or "copyright" in html.lower() else 0,
            'NoOfImage': len(soup.find_all('img')),
            'NoOfCSS': len(soup.find_all('link', rel='stylesheet')),
            'NoOfJS': len(soup.find_all('script')),
            'NoOfSelfRef': html.lower().count('href="#'),
            'NoOfEmptyRef': html.lower().count('href=""'),
            'NoOfExternalRef': html.lower().count('http'),
        }

        return features
    except Exception:
        return {
            'LineOfCode': 0,
            'LargestLineLength': 0,
            'HasTitle': 0,
            'DomainTitleMatchScore': 0,
            'URLTitleMatchScore': 0,
            'HasFavicon': 0,
            'Robots': 0,
            'IsResponsive': 0,
            'NoOfURLRedirect': 0,
            'NoOfSelfRedirect': 0,
            'HasDescription': 0,
            'NoOfPopup': 0,
            'NoOfiFrame': 0,
            'HasExternalFormSubmit': 0,
            'HasSocialNet': 0,
            'HasSubmitButton': 0,
            'HasHiddenFields': 0,
            'HasPasswordField': 0,
            'HasCopyrightInfo': 0,
            'NoOfImage': 0,
            'NoOfCSS': 0,
            'NoOfJS': 0,
            'NoOfSelfRef': 0,
            'NoOfEmptyRef': 0,
            'NoOfExternalRef': 0
        }

def extract_all_features(url):
    base_features, parsed_url, domain, suffix, subdomain = extract_url_base_features(url)
    char_features = extract_char_features(url)
    html_features = extract_html_features(url)

    placeholder_features = {
        'URLSimilarityIndex': 0,
        'CharContinuationRate': 0,
        'TLDLegitimateProb': 0,
        'URLCharProb': 0,
        'HasObfuscation': 0,
        'NoOfObfuscatedChar': 0,
        'ObfuscationRatio': 0,
    }

    return {**base_features, **char_features, **html_features, **placeholder_features}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get("url", "")
    features = extract_all_features(url)
    # data=extract_all_features(data)
    input_df = pd.DataFrame([features])
    print(input_df)
    input_df.to_csv("input_features.csv", index=False)

    # Add missing columns with default value 0
    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0

    # Reorder columns
    input_df = input_df[expected_cols]
    input_df.to_csv("input_features.csv", index=False)
    # Make predictio
    prediction = "bad" if model.predict(input_df)[0] == 1 else "good"
    print(model.predict(input_df)[0])
    return jsonify({'prediction': str(prediction)})


if __name__ == '__main__':
    app.run(debug=True)

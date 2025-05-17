import re
from urllib.parse import urlparse

def extract_features(url):
    return {
        "url_length": len(url),
        "num_dots": url.count('.'),
        "https": int(url.startswith("https")),
        "has_ip": int(bool(re.match(r'\d+\.\d+\.\d+\.\d+', url)))
    }

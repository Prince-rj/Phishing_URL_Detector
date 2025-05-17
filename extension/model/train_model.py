import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load Dataset
df = pd.read_csv("phishing_dataset.csv")

# Feature Selection
X = df.drop(columns=["label"])
y = df["label"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save Model
pickle.dump(model, open("model/phishing_model.pkl", "wb"))

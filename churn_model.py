import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.preprocessing import LabelEncoder

import joblib


df = pd.read_csv(
    'data/churn_labels.csv'
)

encoder = LabelEncoder()

df['subscription_type'] = encoder.fit_transform(
    df['subscription_type']
)

X = df[[
    'avg_session_duration',
    'purchase_count',
    'subscription_type'
]]

y = df['churned']

# --------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# --------------------------------------
# MODEL TRAINING
# --------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

y_pred = model.predict(X_test)
accuracy = accuracy_score(
    y_test,
    y_pred
)

print(f"Model Accuracy: {accuracy:.2f}")

print("Classification Report: ")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("Confusion Matrix: ")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

joblib.dump(
    model,
    'churn_model.pkl'
)

print("Model saved successfully!")

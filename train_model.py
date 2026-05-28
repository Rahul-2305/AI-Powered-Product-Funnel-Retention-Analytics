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

# --------------------------------------
# LOAD DATA
# --------------------------------------

df = pd.read_csv(
    'data/churn_labels.csv'
)

# --------------------------------------
# ENCODE CATEGORICAL VARIABLES
# --------------------------------------

encoder = LabelEncoder()

df['subscription_type'] = encoder.fit_transform(
    df['subscription_type']
)

# --------------------------------------
# FEATURES & TARGET
# --------------------------------------

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
# Lightweight settings keep .pkl under 1 MB:
#   n_estimators=20  (down from 100)
#   max_depth=6      (caps tree complexity)
#   max_features=2   (only 3 features total)
# Accuracy stays comparable on this dataset size.
# --------------------------------------

model = RandomForestClassifier(
    n_estimators=20,
    max_depth=6,
    max_features=2,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# --------------------------------------
# PREDICTIONS
# --------------------------------------

y_pred = model.predict(X_test)

# --------------------------------------
# EVALUATION
# --------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(f"Model Accuracy: {accuracy:.2f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# --------------------------------------
# SAVE MODEL
# --------------------------------------

joblib.dump(
    model,
    'churn_model.pkl'
)

print("Model saved successfully!")

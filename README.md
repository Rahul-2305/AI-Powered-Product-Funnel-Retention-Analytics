# 🤖 AI-Powered Product Funnel & Retention Analytics Dashboard

A Streamlit dashboard that combines product analytics, ML-based churn prediction, and AI-generated insights to help product teams understand user behaviour across the full acquisition-to-retention funnel.

## ✨ Features

- **Product Funnel** — Visual funnel from App Visits → Signups → Onboarding → Purchase → Repeat Purchase
- **Churn Prediction** — Random Forest model flags high-risk users with a churn probability score
- **Session Engagement** — Average session duration segmented by platform
- **AI Executive Summary** — Gemini 2.0 Flash generates a business-focused narrative; falls back to local rule-based engine if unavailable
- **Filters** — Slice every chart by Device Type and Acquisition Channel

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Create `.streamlit/secrets.toml` (this file is git-ignored — never commit it):
```toml
GEMINI_API_KEY = "your-key-here"
```
Get a free key at [aistudio.google.com](https://aistudio.google.com).  
The app works without it — it falls back to the local AI engine automatically.

### 4. Run the app
```bash
streamlit run app.py
```

`setup.py` runs automatically on first launch and:
- Generates synthetic datasets inside `data/` (~1.8 MB total)
- Trains and saves the churn model (`churn_model.pkl`, ~112 KB)

Both are git-ignored and re-created locally, so the repo stays lightweight.

## 🗂 Project Structure

```
├── app.py                # Main Streamlit dashboard
├── ai_engine.py          # Rule-based AI insight engine (fallback)
├── gemini_engine.py      # Gemini 2.0 Flash integration
├── generate_data.py      # Synthetic dataset generator (2,000 users)
├── train_model.py        # Random Forest churn model trainer
├── churn_model.py        # Standalone model training script
├── setup.py              # Auto-generates data + model on first run
├── requirements.txt      # Python dependencies
└── data/                 # ← git-ignored, generated at runtime
    ├── users.csv
    ├── sessions.csv
    ├── user_events.csv
    ├── purchases.csv
    └── churn_labels.csv
```

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit, Plotly, HTML/CSS |
| ML | scikit-learn (Random Forest) |
| AI | Google Gemini 2.0 Flash |
| Data | pandas, NumPy, Faker |

## 👤 Author

**Beeraboina Rahul** — [Portfolio](https://beeraboina-rahul-website.streamlit.app/)

---
*© 2026 Beeraboina Rahul*
"# AI-Powered-Product-Funnel-Retention-Analytics" 

import os

if not os.path.exists("data/user_events.csv"):

    print("Generating datasets...")
    import generate_data
if not os.path.exists("churn_model.pkl"):

    print("Training churn model...")

    import churn_model

import os
import pandas as pd
import numpy as np
import random

from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# ----------------------------------
# CONFIG
# ----------------------------------

NUM_USERS = 2000          # Reduced from 15000 → keeps CSVs well under 5 MB

countries = ['India', 'USA', 'UK', 'Canada']

channels = [
    'Google Ads',
    'Instagram',
    'Referral',
    'Organic',
    'YouTube'
]

devices = ['Android', 'iOS', 'Web']

age_groups = [
    '18-24',
    '25-34',
    '35-44',
    '45+'
]

subscription_types = [
    'Free',
    'Premium'
]

event_types = [
    'app_visit',
    'signup',
    'onboarding_complete',
    'search',
    'add_to_cart',
    'purchase',
    'repeat_purchase',
    'notification_click',
    'uninstall'
]

product_categories = [
    'Food',
    'Electronics',
    'Fashion',
    'Entertainment'
]

payment_methods = [
    'UPI',
    'Credit Card',
    'PayPal',
    'Debit Card'
]

# ----------------------------------
# USERS TABLE
# ----------------------------------

users = []

start_date = datetime(2024, 1, 1)

for user_id in range(1, NUM_USERS + 1):

    signup_date = start_date + timedelta(
        days=random.randint(0, 730)
    )

    device = random.choices(
        devices,
        weights=[55, 30, 15]
    )[0]

    subscription = random.choices(
        subscription_types,
        weights=[80, 20]
    )[0]

    users.append({
        'user_id': user_id,
        'signup_date': signup_date,
        'acquisition_channel': random.choice(channels),
        'device_type': device,
        'country': random.choice(countries),
        'age_group': random.choice(age_groups),
        'subscription_type': subscription
    })

users_df = pd.DataFrame(users)

# ----------------------------------
# SESSIONS TABLE
# ----------------------------------

sessions = []

session_id = 1

for user in users:

    num_sessions = np.random.poisson(3)  # Reduced from 5 → fewer rows

    if num_sessions < 1:
        num_sessions = 1

    for _ in range(num_sessions):

        session_start = user['signup_date'] + timedelta(
            days=random.randint(0, 120),
            minutes=random.randint(0, 1440)
        )

        if user['subscription_type'] == 'Premium':
            duration = random.uniform(8, 45)
        else:
            duration = random.uniform(1, 20)

        pages_viewed = int(duration / 2)

        sessions.append({
            'session_id': session_id,
            'user_id': user['user_id'],
            'session_start': session_start,
            'session_end': session_start + timedelta(minutes=duration),
            'session_duration_minutes': round(duration, 2),
            'pages_viewed': pages_viewed,
            'platform': user['device_type']
        })

        session_id += 1

sessions_df = pd.DataFrame(sessions)

# ----------------------------------
# USER EVENTS TABLE
# ----------------------------------

events = []

event_id = 1

for session in sessions:

    user_id = session['user_id']

    session_events = ['app_visit']

    if random.random() < 0.7:
        session_events.append('signup')

    if 'signup' in session_events and random.random() < 0.6:
        session_events.append('onboarding_complete')

    if random.random() < 0.8:
        session_events.append('search')

    if random.random() < 0.4:
        session_events.append('add_to_cart')

    if random.random() < 0.25:
        session_events.append('purchase')

    if 'purchase' in session_events and random.random() < 0.3:
        session_events.append('repeat_purchase')

    if random.random() < 0.05:
        session_events.append('uninstall')

    for event in session_events:

        events.append({
            'event_id': event_id,
            'user_id': user_id,
            'event_time': session['session_start'] + timedelta(
                minutes=random.randint(0, 60)
            ),
            'event_type': event,
            'session_id': session['session_id'],
            'feature_name': random.choice([
                'Search',
                'Checkout',
                'Recommendations',
                'Profile',
                'Notifications'
            ])
        })

        event_id += 1

events_df = pd.DataFrame(events)

# ----------------------------------
# PURCHASES TABLE
# ----------------------------------

purchase_events = events_df[
    events_df['event_type'].isin(
        ['purchase', 'repeat_purchase']
    )
]

purchases = []

purchase_id = 1

for _, row in purchase_events.iterrows():

    order_value = round(
        random.uniform(5, 500),
        2
    )

    purchases.append({
        'purchase_id': purchase_id,
        'user_id': row['user_id'],
        'purchase_time': row['event_time'],
        'product_category': random.choice(
            product_categories
        ),
        'order_value': order_value,
        'payment_method': random.choice(
            payment_methods
        )
    })

    purchase_id += 1

purchases_df = pd.DataFrame(purchases)

# ----------------------------------
# CHURN LABELS
# ----------------------------------

churn_labels = []

for user in users:

    user_sessions = sessions_df[
        sessions_df['user_id'] == user['user_id']
    ]

    avg_duration = user_sessions[
        'session_duration_minutes'
    ].mean()

    purchase_count = len(
        purchases_df[
            purchases_df['user_id'] == user['user_id']
        ]
    )

    churn_probability = 0

    if avg_duration < 5:
        churn_probability += 0.4

    if purchase_count == 0:
        churn_probability += 0.4

    if user['subscription_type'] == 'Free':
        churn_probability += 0.2

    churned = 1 if random.random() < churn_probability else 0

    churn_labels.append({
        'user_id': user['user_id'],
        'avg_session_duration': round(avg_duration, 2),
        'purchase_count': purchase_count,
        'subscription_type': user['subscription_type'],
        'churned': churned
    })

churn_df = pd.DataFrame(churn_labels)

# ----------------------------------
# SAVE FILES
# ----------------------------------

os.makedirs('data', exist_ok=True)

users_df.to_csv('data/users.csv', index=False)
sessions_df.to_csv('data/sessions.csv', index=False)
events_df.to_csv('data/user_events.csv', index=False)
purchases_df.to_csv('data/purchases.csv', index=False)
churn_df.to_csv('data/churn_labels.csv', index=False)

print("AI-ready datasets generated successfully!")
print(f"  users.csv        → {len(users_df):,} rows")
print(f"  sessions.csv     → {len(sessions_df):,} rows")
print(f"  user_events.csv  → {len(events_df):,} rows")
print(f"  purchases.csv    → {len(purchases_df):,} rows")
print(f"  churn_labels.csv → {len(churn_df):,} rows")

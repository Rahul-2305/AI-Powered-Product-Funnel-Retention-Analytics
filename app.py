import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from gemini_engine import generate_ai_summary
from ai_engine import AIInsightEngine
import joblib

model = joblib.load(
    'churn_model.pkl'
)
st.set_page_config(
    page_title="AI Product Analytics Dashboard",
    layout="wide"
)

st.title("🤖 AI-Powered Product Funnel & Retention Analytics Dashboard")


users_df = pd.read_csv('data/users.csv')
sessions_df = pd.read_csv('data/sessions.csv')
events_df = pd.read_csv('data/user_events.csv')
purchases_df = pd.read_csv('data/purchases.csv')
churn_df = pd.read_csv('data/churn_labels.csv')


users_df['signup_date'] = pd.to_datetime(users_df['signup_date'])
sessions_df['session_start'] = pd.to_datetime(sessions_df['session_start'])
events_df['event_time'] = pd.to_datetime(events_df['event_time'])


st.sidebar.header("Dashboard Filters")

selected_device = st.sidebar.multiselect(
    "Device Type",
    users_df['device_type'].unique(),
    default=users_df['device_type'].unique()
)

selected_channel = st.sidebar.multiselect(
    "Acquisition Channel",
    users_df['acquisition_channel'].unique(),
    default=users_df['acquisition_channel'].unique()
)

filtered_users = users_df[
    (users_df['device_type'].isin(selected_device)) &
    (users_df['acquisition_channel'].isin(selected_channel))
]

filtered_user_ids = filtered_users['user_id']

filtered_sessions = sessions_df[
    sessions_df['user_id'].isin(filtered_user_ids)
]

filtered_events = events_df[
    events_df['user_id'].isin(filtered_user_ids)
]

filtered_purchases = purchases_df[
    purchases_df['user_id'].isin(filtered_user_ids)
]

filtered_churn = churn_df[
    churn_df['user_id'].isin(filtered_user_ids)
]


unique_users = filtered_users['user_id'].nunique()

avg_session_duration = round(
    filtered_sessions['session_duration_minutes'].mean(),
    2
)

purchase_count = len(filtered_purchases)

retention_rate = round(
    (
        filtered_events[
            filtered_events['event_type'] == 'repeat_purchase'
        ]['user_id'].nunique()
        /
        unique_users
    ) * 100,
    2
)

churn_rate = round(
    filtered_churn['churned'].mean() * 100,
    2
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Users",
    f"{unique_users:,}"
)

col2.metric(
    "⏱ Avg Session",
    f"{avg_session_duration} mins"
)

col3.metric(
    "🔁 Retention Rate",
    f"{retention_rate}%"
)

col4.metric(
    "⚠️ Churn Rate",
    f"{churn_rate}%"
)

st.divider()


ai_engine = AIInsightEngine()

prediction_features = filtered_churn[[

    'avg_session_duration',
    'purchase_count',
    'subscription_type'

]].copy()

# Encode subscription type

prediction_features['subscription_type'] = (
    prediction_features['subscription_type']
    .map({
        'Free': 0,
        'Premium': 1
    })
)

filtered_churn['churn_prediction'] = model.predict(
    prediction_features
)

filtered_churn['churn_probability'] = (

    model.predict_proba(
        prediction_features
    )[:, 1]

) * 100


visit_users = filtered_events[
    filtered_events['event_type'] == 'app_visit'
]['user_id'].nunique()

signup_users = filtered_events[
    filtered_events['event_type'] == 'signup'
]['user_id'].nunique()

onboarding_users = filtered_events[
    filtered_events['event_type'] == 'onboarding_complete'
]['user_id'].nunique()

purchase_users = filtered_events[
    filtered_events['event_type'] == 'purchase'
]['user_id'].nunique()

repeat_users = filtered_events[
    filtered_events['event_type'] == 'repeat_purchase'
]['user_id'].nunique()


ai_engine.analyze_funnel(
    visit_users,
    signup_users,
    onboarding_users,
    purchase_users,
    repeat_users
)

# Retention analysis

ai_engine.analyze_retention(
    retention_rate,
    churn_rate
)

# Engagement analysis

avg_pages_viewed = filtered_sessions[
    'pages_viewed'
].mean()

ai_engine.analyze_engagement(
    avg_session_duration,
    avg_pages_viewed
)


# --------------------------------------
# CUSTOM HTML FUNNEL
# --------------------------------------

st.subheader("📊 Product Funnel")

funnel_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{
    background-color: transparent;
}}

.funnel-container {{
    width: 100%;
    text-align: center;
    margin-top: 20px;
    font-family: Arial, sans-serif;
}}

.funnel-step {{
    margin: auto;
    color: white;
    padding: 20px;
    margin-bottom: 12px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    transition: transform 0.2s ease;
}}

.funnel-step:hover {{
    transform: scale(1.02);
}}

.step1 {{
    width: 90%;
    background: linear-gradient(90deg, #4338CA, #6366F1);
}}

.step2 {{
    width: 72%;
    background: linear-gradient(90deg, #2563EB, #3B82F6);
}}

.step3 {{
    width: 56%;
    background: linear-gradient(90deg, #0891B2, #06B6D4);
}}

.step4 {{
    width: 40%;
    background: linear-gradient(90deg, #0F766E, #14B8A6);
}}

.step5 {{
    width: 26%;
    background: linear-gradient(90deg, #166534, #22C55E);
}}

</style>
</head>

<body>

<div class="funnel-container">

    <div class="funnel-step step1">
        👀 App Visits<br>
        {visit_users:,}
    </div>

    <div class="funnel-step step2">
        📝 Signups<br>
        {signup_users:,}
    </div>

    <div class="funnel-step step3">
        ✅ Onboarding Complete<br>
        {onboarding_users:,}
    </div>

    <div class="funnel-step step4">
        💳 Purchases<br>
        {purchase_users:,}
    </div>

    <div class="funnel-step step5">
        🔁 Repeat Purchases<br>
        {repeat_users:,}
    </div>

</div>

</body>
</html>
"""

components.html(
    funnel_html,
    height=650,
    scrolling=False
)
st.divider()

st.subheader("📋 Funnel Conversion Analysis")

funnel_steps = [
    ("App Visits", visit_users),
    ("Signups", signup_users),
    ("Onboarding Complete", onboarding_users),
    ("Purchases", purchase_users),
    ("Repeat Purchases", repeat_users)
]

funnel_table = []

previous_users = None

for stage, users in funnel_steps:

    if previous_users is None:
        conversion_rate = 100
        dropoff_rate = 0
    else:
        conversion_rate = round(
            (users / previous_users) * 100,
            2
        )

        dropoff_rate = round(
            100 - conversion_rate,
            2
        )

    funnel_table.append({
        "Funnel Stage": stage,
        "Users": f"{users:,}",
        "Conversion %": f"{conversion_rate}%",
        "Drop-off %": f"{dropoff_rate}%"
    })

    previous_users = users

funnel_df = pd.DataFrame(funnel_table)

styled_funnel = funnel_df.style\
    .highlight_max(
        subset=['Conversion %'],
        color='green'
    )

st.dataframe(
    styled_funnel,
    hide_index=True,
    use_container_width=True
)
st.divider()

st.subheader("📈 Retention Analysis")

retention_data = filtered_events[
    filtered_events['event_type'].isin([
        'purchase',
        'repeat_purchase'
    ])
]

retention_summary = (
    retention_data
    .groupby('event_type')['user_id']
    .nunique()
    .reset_index()
)

fig_retention = px.bar(
    retention_summary,
    x='event_type',
    y='user_id',
    color='event_type',
    title='Purchase vs Repeat Purchase Users'
)

st.plotly_chart(
    fig_retention,
    use_container_width=True
)

# --------------------------------------
# SESSION ENGAGEMENT
# --------------------------------------

st.subheader("📱 Session Engagement")

session_summary = (
    filtered_sessions
    .groupby('platform')['session_duration_minutes']
    .mean()
    .reset_index()
)

fig_session = px.bar(
    session_summary,
    x='platform',
    y='session_duration_minutes',
    color='platform',
    title='Average Session Duration by Platform'
)

st.plotly_chart(
    fig_session,
    use_container_width=True
)

# --------------------------------------
# CHURN ANALYSIS
# --------------------------------------

st.subheader("⚠️ Churn Analysis")

churn_summary = (
    filtered_churn
    .groupby('subscription_type')['churned']
    .mean()
    .reset_index()
)

churn_summary['churned'] = churn_summary['churned'] * 100

fig_churn = px.bar(
    churn_summary,
    x='subscription_type',
    y='churned',
    color='subscription_type',
    title='Churn Rate by Subscription Type'
)

st.plotly_chart(
    fig_churn,
    use_container_width=True
)


st.subheader("🚀 Acquisition Channel Performance")

channel_summary = (
    filtered_users
    .groupby('acquisition_channel')['user_id']
    .count()
    .reset_index()
)

fig_channel = px.pie(
    channel_summary,
    names='acquisition_channel',
    values='user_id',
    title='User Acquisition Distribution'
)

st.plotly_chart(
    fig_channel,
    use_container_width=True
)

st.divider()

st.subheader("⚠️ High Churn Risk Users")

high_risk_users = filtered_churn[
    filtered_churn['churn_probability'] > 75
]

high_risk_display = high_risk_users[[

    'user_id',
    'avg_session_duration',
    'purchase_count',
    'subscription_type',
    'churn_probability'

]].copy()

high_risk_display['churn_probability'] = (
    high_risk_display['churn_probability']
    .round(2)
)

st.dataframe(
    high_risk_display.head(20),
    use_container_width=True,
    hide_index=True
)

signup_conversion = round(
    (signup_users / visit_users) * 100,
    2
) if visit_users > 0 else 0

purchase_conversion = round(
    (purchase_users / onboarding_users) * 100,
    2
) if onboarding_users > 0 else 0

st.divider()

st.subheader("🤖 AI Product Analyst Assistant")

if st.button("Generate AI Executive Summary"):

    with st.spinner("Generating AI insights..."):

        # ----------------------------------------
        # TRY GEMINI AI
        # ----------------------------------------

        ai_response = generate_ai_summary(

            retention_rate,
            churn_rate,
            avg_session_duration,
            signup_conversion,
            purchase_conversion

        )

        # ----------------------------------------
        # GEMINI SUCCESS
        # ----------------------------------------

        if ai_response["success"]:

            st.success(
                "Gemini AI Analysis Generated"
            )

            st.markdown(
                ai_response["content"]
            )

        # ----------------------------------------
        # FALLBACK TO LOCAL AI ENGINE
        # ----------------------------------------

        else:

            st.warning(
                "Gemini AI unavailable. Using local AI engine."
            )

            fallback_summary = (
                ai_engine.generate_fallback_summary()
            )

            st.markdown(
                fallback_summary
            )

st.divider()

with st.expander("About this App"):
    st.write("Created by Beeraboina Rahul")
    st.write("Made in Python & Streamlit")
    st.write(
        "Know more about Beeraboina Rahul at https://beeraboina-rahul-website.streamlit.app/")


st.caption("© 2026 Beeraboina Rahul")

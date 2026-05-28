from google import genai
import streamlit as st

# ----------------------------------------
# CONFIGURE GEMINI CLIENT
# ----------------------------------------

client = genai.Client(

    api_key=st.secrets[
        "GEMINI_API_KEY"
    ]

)


def generate_ai_summary(

    retention_rate,
    churn_rate,
    avg_session_duration,
    signup_conversion,
    purchase_conversion

):

    prompt = f"""

    You are a senior Product Analyst.

    Analyze the following product metrics and provide:

    1. Executive Summary
    2. Key Risks
    3. Product Recommendations
    4. Growth Opportunities

    Product Metrics:

    - Retention Rate: {retention_rate:.2f}%
    - Churn Rate: {churn_rate:.2f}%
    - Avg Session Duration: {avg_session_duration:.2f} mins
    - Signup Conversion: {signup_conversion:.2f}%
    - Purchase Conversion: {purchase_conversion:.2f}%

    Keep response concise, professional, and business-focused.

    """

    try:

        response = client.models.generate_content(

            model="gemini-2.0-flash",

            contents=prompt

        )

        return {
            "success": True,
            "content": response.text
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

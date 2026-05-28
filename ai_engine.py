import pandas as pd

# ----------------------------------------
# AI INSIGHT ENGINE
# ----------------------------------------


class AIInsightEngine:

    def __init__(self):

        self.insights = []
        self.recommendations = []
        self.severity = []

    # ----------------------------------------
    # ADD INSIGHT
    # ----------------------------------------

    def add_insight(
        self,
        level,
        insight,
        recommendation
    ):

        self.severity.append(level)

        self.insights.append(insight)

        self.recommendations.append(
            recommendation
        )

    # ----------------------------------------
    # FUNNEL ANALYSIS
    # ----------------------------------------

    def analyze_funnel(
        self,
        visit_users,
        signup_users,
        onboarding_users,
        purchase_users,
        repeat_users
    ):

        signup_conversion = (
            signup_users / visit_users
        ) * 100

        onboarding_conversion = (
            onboarding_users / signup_users
        ) * 100

        purchase_conversion = (
            purchase_users / onboarding_users
        ) * 100

        repeat_conversion = (
            repeat_users / purchase_users
        ) * 100

        # Signup Drop

        if signup_conversion < 60:

            self.add_insight(
                "HIGH",
                f"Signup conversion is critically low at {signup_conversion:.2f}%.",
                "Simplify signup flow and reduce onboarding friction."
            )

        # Onboarding Drop

        if onboarding_conversion < 70:

            self.add_insight(
                "MEDIUM",
                f"Onboarding completion rate dropped to {onboarding_conversion:.2f}%.",
                "Improve onboarding UX and reduce unnecessary steps."
            )

        # Purchase Drop

        if purchase_conversion < 40:

            self.add_insight(
                "HIGH",
                f"Purchase conversion is weak at {purchase_conversion:.2f}%.",
                "Optimize checkout experience and improve recommendation relevance."
            )

        # Retention Drop

        if repeat_conversion < 35:

            self.add_insight(
                "HIGH",
                f"Repeat purchase conversion is low at {repeat_conversion:.2f}%.",
                "Introduce loyalty programs and personalized notifications."
            )

    # ----------------------------------------
    # RETENTION ANALYSIS
    # ----------------------------------------

    def analyze_retention(
        self,
        retention_rate,
        churn_rate
    ):

        if retention_rate < 25:

            self.add_insight(
                "HIGH",
                f"Retention rate is critically low at {retention_rate:.2f}%.",
                "Improve long-term engagement and post-purchase retention."
            )

        elif retention_rate < 40:

            self.add_insight(
                "MEDIUM",
                f"Retention rate is below benchmark at {retention_rate:.2f}%.",
                "Increase re-engagement campaigns and improve product stickiness."
            )

        if churn_rate > 50:

            self.add_insight(
                "HIGH",
                f"Churn rate is extremely high at {churn_rate:.2f}%.",
                "Investigate onboarding friction and user dissatisfaction."
            )

        elif churn_rate > 35:

            self.add_insight(
                "MEDIUM",
                f"Churn rate is elevated at {churn_rate:.2f}%.",
                "Analyze churn cohorts and identify high-risk users."
            )

    # ----------------------------------------
    # SESSION ANALYSIS
    # ----------------------------------------

    def analyze_engagement(
        self,
        avg_session_duration,
        pages_viewed
    ):

        if avg_session_duration < 5:

            self.add_insight(
                "HIGH",
                f"Average session duration is critically low at {avg_session_duration:.2f} minutes.",
                "Improve product discovery and content engagement."
            )

        elif avg_session_duration < 10:

            self.add_insight(
                "MEDIUM",
                f"Users spend limited time in-app ({avg_session_duration:.2f} mins).",
                "Introduce personalized recommendations and sticky features."
            )

        if pages_viewed < 4:

            self.add_insight(
                "LOW",
                f"Average pages viewed per session is only {pages_viewed:.2f}.",
                "Improve internal navigation and feature discoverability."
            )

    # ----------------------------------------
    # GENERATE EXECUTIVE SUMMARY
    # ----------------------------------------

    def generate_summary(self):

        if len(self.insights) == 0:

            return (
                "Product metrics are currently performing within healthy operational thresholds."
            )

        summary = (
            "AI analysis detected multiple product performance signals requiring attention. "
        )

        high_issues = self.severity.count("HIGH")

        medium_issues = self.severity.count("MEDIUM")

        low_issues = self.severity.count("LOW")

        summary += (
            f"{high_issues} high severity issues, "
            f"{medium_issues} medium severity issues, "
            f"and {low_issues} low severity observations were identified."
        )

        return summary

    # ----------------------------------------
    # EXPORT RESULTS
    # ----------------------------------------

    def get_results(self):

        return pd.DataFrame({

            'Severity': self.severity,
            'Insight': self.insights,
            'Recommendation': self.recommendations

        })

    def generate_fallback_summary(self):

        summary = "## 🤖 AI Executive Summary\n\n"

        if len(self.insights) == 0:

            summary += (
                "Product performance is currently within healthy thresholds.\n"
            )

        else:

            summary += (
                "Multiple product performance issues and optimization opportunities were detected.\n\n"
            )

            summary += "### 📌 Key Insights\n\n"

            for insight in self.insights:

                summary += f"- {insight}\n"

            summary += "\n### 💡 Recommendations\n\n"

            for rec in self.recommendations:

                summary += f"- {rec}\n"

        return summary

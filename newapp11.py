import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="LoyalLens",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------------
# PREMIUM UI (SAFE CLEAN VERSION)
# ----------------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0b0f19, #0a0d14);
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 2.5rem 3rem;
}

h1, h2, h3 {
    color: white;
    font-weight: 600;
}

p, span {
    color: rgba(255,255,255,0.75);
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HEADER
# ----------------------------------
st.title("🚀 LoyalLens")
st.markdown("### AI-Powered Customer Loyalty Intelligence Platform")
st.caption("Analyze customers, predict churn risk, and optimize retention strategies.")

# ----------------------------------
# FILE UPLOAD
# ----------------------------------
uploaded_file = st.file_uploader(
    "Upload your customer CSV file",
    type=["csv"]
)

# ----------------------------------
# MAIN APP
# ----------------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    # ----------------------------------
    # PREVIEW
    # ----------------------------------
    with st.expander("📊 Data Preview"):
        st.dataframe(df.head(), use_container_width=True)

    columns = list(df.columns)

    # ----------------------------------
    # COLUMN MAPPING
    # ----------------------------------
    st.markdown("## 🤖 Column Mapping")

    customer_id_col = st.selectbox("Customer ID", columns)
    order_value_col = st.selectbox("Order Value", columns)

    discount_col = st.selectbox(
        "Discount Column",
        ["Not Available"] + columns
    )

    customer_name_col = st.selectbox(
        "Customer Name Column",
        ["Not Available"] + columns
    )

    # ----------------------------------
    # LOYALTY ENGINE
    # ----------------------------------
    analysis_df = df.copy()

    max_value = analysis_df[order_value_col].max()

    analysis_df["Loyalty Score"] = (
        analysis_df[order_value_col] / max_value
    ) * 100 if max_value > 0 else 0

    # Discount adjustment (if available)
    if discount_col != "Not Available":
        max_discount = analysis_df[discount_col].max()

        if max_discount > 0:
            discount_score = (
                1 - (analysis_df[discount_col] / max_discount)
            ) * 30

            analysis_df["Loyalty Score"] = (
                analysis_df["Loyalty Score"] * 0.7
                + discount_score
            )

    analysis_df["Loyalty Score"] = analysis_df["Loyalty Score"].clip(0, 100)

    def categorize(score):
        if score >= 80:
            return "Loyal Customer"
        elif score >= 50:
            return "Potential Loyalist"
        return "At Risk"

    analysis_df["Customer Category"] = analysis_df["Loyalty Score"].apply(categorize)

    # ----------------------------------
    # KPI DASHBOARD
    # ----------------------------------
    st.markdown("## 📊 Dashboard Overview")

    total = len(analysis_df)
    loyal = len(analysis_df[analysis_df["Customer Category"] == "Loyal Customer"])
    potential = len(analysis_df[analysis_df["Customer Category"] == "Potential Loyalist"])
    risk = len(analysis_df[analysis_df["Customer Category"] == "At Risk"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Customers", total)

    with col2:
        st.metric("Loyal", loyal)

    with col3:
        st.metric("Potential", potential)

    with col4:
        st.metric("At Risk", risk)

    # ----------------------------------
    # BUSINESS INSIGHTS
    # ----------------------------------
    st.markdown("## 📌 Insights")

    loyal_pct = round((loyal / total) * 100, 1)
    potential_pct = round((potential / total) * 100, 1)
    risk_pct = round((risk / total) * 100, 1)

    st.write(f"🟢 {loyal_pct}% Loyal Customers")
    st.write(f"🟡 {potential_pct}% Potential Loyalists")
    st.write(f"🔴 {risk_pct}% At Risk Customers")

    if risk_pct > 50:
        st.warning("High churn risk detected. Immediate retention strategy needed.")
    elif loyal_pct > 50:
        st.success("Strong customer loyalty base.")
    else:
        st.info("Balanced customer distribution.")

    # ----------------------------------
    # REVENUE ANALYSIS (RESTORED)
    # ----------------------------------
    st.markdown("## 💰 Revenue Analysis")

    total_revenue = df[order_value_col].sum()
    avg_order_value = df[order_value_col].mean()

    risk_revenue = risk * avg_order_value

    st.success(f"Total Revenue: ${total_revenue:,.2f}")
    st.error(f"Estimated Revenue at Risk: ${risk_revenue:,.2f}")
    st.write(f"Average Order Value: ${avg_order_value:,.2f}")

    # ----------------------------------
    # EXECUTIVE SUMMARY (RESTORED)
    # ----------------------------------
    st.markdown("## 📄 Executive Summary")

    st.info(f"""
Total Revenue: ${total_revenue:,.2f}

Loyal Customers: {loyal_pct}%

Potential Loyalists: {potential_pct}%

At Risk Customers: {risk_pct}%

Estimated Revenue at Risk: ${risk_revenue:,.2f}

Recommendation: Focus on At Risk customers and convert Potential Loyalists into Loyal Customers.
""")

    # ----------------------------------
    # CHARTS
    # ----------------------------------
    st.markdown("## 📈 Customer Distribution")

    category_counts = analysis_df["Customer Category"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(category_counts)

    with col2:
        fig = px.pie(
            names=category_counts.index,
            values=category_counts.values,
            title="Customer Segments"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------
    # TOP CUSTOMERS
    # ----------------------------------
    st.markdown("## 🏆 Top Loyal Customers")

    st.dataframe(
        analysis_df.sort_values("Loyalty Score", ascending=False).head(10),
        use_container_width=True
    )

    # ----------------------------------
    # CUSTOMER SEARCH (RESTORED)
    # ----------------------------------
    st.markdown("## 🔍 Customer Search")

    search_id = st.text_input("Enter Customer ID")

    if search_id:
        result = analysis_df[
            analysis_df[customer_id_col].astype(str) == search_id
        ]

        if not result.empty:
            st.success("Customer Found")

            customer = result.iloc[0]

            st.write(f"**ID:** {customer[customer_id_col]}")
            st.write(f"**Loyalty Score:** {int(customer['Loyalty Score'])}")
            st.write(f"**Category:** {customer['Customer Category']}")

            if customer["Customer Category"] == "Loyal Customer":
                st.success("Recommended: VIP rewards & referrals")
            elif customer["Customer Category"] == "Potential Loyalist":
                st.info("Recommended: Targeted engagement offers")
            else:
                st.warning("Recommended: Retention campaign needed")
        else:
            st.warning("Customer not found")

    # ----------------------------------
    # DOWNLOAD
    # ----------------------------------
    st.markdown("## ⬇ Download Results")

    csv = analysis_df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "loyallens_analysis.csv",
        "text/csv"
    )

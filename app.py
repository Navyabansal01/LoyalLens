# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # ----------------------------------
# # PAGE CONFIG
# # ----------------------------------
# st.set_page_config(
#     page_title="LoyalLens",
#     page_icon="🚀",
#     layout="wide"
# )

# # ----------------------------------
# # PREMIUM STARTUP UI THEME
# # ----------------------------------
# st.markdown("""
# <style>

# [data-testid="stAppViewContainer"] {
#     background: radial-gradient(circle at top, #111827, #0b0f19);
# }

# #MainMenu, footer, header {
#     visibility: hidden;
# }

# .block-container {
#     padding: 2.2rem 3rem;
# }

# /* Typography */
# h1, h2, h3 {
#     color: white;
#     font-weight: 600;
#     letter-spacing: 0.3px;
# }

# p, span {
#     color: rgba(255,255,255,0.75);
# }

# /* Metric cards (startup SaaS feel) */
# [data-testid="stMetric"] {
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.06);
#     padding: 14px;
#     border-radius: 14px;
#     box-shadow: 0 8px 30px rgba(0,0,0,0.25);
# }

# /* Buttons */
# .stButton > button {
#     background: linear-gradient(90deg, #6366f1, #8b5cf6);
#     color: white;
#     border-radius: 10px;
#     border: none;
#     padding: 0.55rem 1.2rem;
#     font-weight: 600;
#     transition: all 0.2s ease-in-out;
# }

# .stButton > button:hover {
#     transform: translateY(-2px);
# }

# /* Inputs */
# input, textarea, select {
#     border-radius: 10px !important;
# }

# </style>
# """, unsafe_allow_html=True)

# # ----------------------------------
# # HEADER (STARTUP STYLE)
# # ----------------------------------
# st.title("🚀 LoyalLens")
# st.markdown("### AI Customer Loyalty & Retention Intelligence")
# st.caption("Analyze customers, detect churn risk, and maximize lifetime value.")

# # ----------------------------------
# # FILE UPLOAD
# # ----------------------------------
# uploaded_file = st.file_uploader("Upload Customer CSV", type=["csv"])

# # ----------------------------------
# # MAIN APP
# # ----------------------------------
# if uploaded_file:

#     df = pd.read_csv(uploaded_file)
#     st.success("Dataset loaded successfully!")

#     # ----------------------------------
#     # DATA PREVIEW (COLLAPSIBLE)
#     # ----------------------------------
#     with st.expander("📊 Data Preview"):
#         st.dataframe(df.head(), use_container_width=True)

#     columns = list(df.columns)

#     # ----------------------------------
#     # COLUMN MAPPING
#     # ----------------------------------
#     st.markdown("## ⚙️ Data Mapping")

#     customer_id_col = st.selectbox("Customer ID Column", columns)
#     order_value_col = st.selectbox("Order Value Column", columns)

#     discount_col = st.selectbox(
#         "Discount Column",
#         ["Not Available"] + columns
#     )

#     # ----------------------------------
#     # LOYALTY ENGINE
#     # ----------------------------------
#     analysis_df = df.copy()

#     max_value = analysis_df[order_value_col].max()

#     analysis_df["Loyalty Score"] = (
#         analysis_df[order_value_col] / max_value * 100
#         if max_value > 0 else 0
#     )

#     # Discount adjustment
#     if discount_col != "Not Available":
#         max_discount = analysis_df[discount_col].max()

#         if max_discount > 0:
#             discount_score = (1 - analysis_df[discount_col] / max_discount) * 30
#             analysis_df["Loyalty Score"] = (
#                 analysis_df["Loyalty Score"] * 0.7 + discount_score
#             )

#     analysis_df["Loyalty Score"] = analysis_df["Loyalty Score"].clip(0, 100)

#     # Category
#     def categorize(score):
#         if score >= 80:
#             return "Loyal Customer"
#         elif score >= 50:
#             return "Potential Loyalist"
#         return "At Risk"

#     analysis_df["Customer Category"] = analysis_df["Loyalty Score"].apply(categorize)

#     # ----------------------------------
#     # DASHBOARD KPIs (STARTUP GRID)
#     # ----------------------------------
#     st.markdown("## 📊 Growth Dashboard")

#     total = len(analysis_df)
#     loyal = len(analysis_df[analysis_df["Customer Category"] == "Loyal Customer"])
#     potential = len(analysis_df[analysis_df["Customer Category"] == "Potential Loyalist"])
#     risk = len(analysis_df[analysis_df["Customer Category"] == "At Risk"])

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric("Total Customers", total)

#     with col2:
#         st.metric("Loyal", loyal)

#     with col3:
#         st.metric("Potential", potential)

#     with col4:
#         st.metric("At Risk", risk)

#     # ----------------------------------
#     # INSIGHTS (WITH % CHANGE VIEW)
#     # ----------------------------------
#     st.markdown("## 📌 Customer Health Insights")

#     loyal_pct = round((loyal / total) * 100, 1)
#     potential_pct = round((potential / total) * 100, 1)
#     risk_pct = round((risk / total) * 100, 1)

#     st.write(f"🟢 Loyal Customers: {loyal_pct}%")
#     st.write(f"🟡 Potential Loyalists: {potential_pct}%")
#     st.write(f"🔴 At Risk Customers: {risk_pct}%")

#     if risk_pct > 50:
#         st.warning("⚠️ High churn risk detected — urgent retention strategy needed.")
#     elif loyal_pct > 50:
#         st.success("💎 Strong customer loyalty base detected.")
#     else:
#         st.info("📊 Balanced customer distribution with growth opportunity.")

#     # ----------------------------------
#     # REVENUE + RISK ANALYSIS
#     # ----------------------------------
#     st.markdown("## 💰 Revenue Intelligence")

#     total_revenue = df[order_value_col].sum()
#     avg_order_value = df[order_value_col].mean()

#     risk_revenue = risk * avg_order_value

#     col1, col2 = st.columns(2)

#     with col1:
#         st.success(f"Total Revenue: ${total_revenue:,.2f}")

#     with col2:
#         st.error(f"Revenue at Risk: ${risk_revenue:,.2f}")

#     st.caption(f"Average Order Value: ${avg_order_value:,.2f}")

#     # ----------------------------------
#     # EXECUTIVE SUMMARY (RESTORED)
#     # ----------------------------------
#     st.markdown("## 📄 Executive Summary")

#     st.info(f"""
# Total Revenue: ${total_revenue:,.2f}

# Loyal Customers: {loyal_pct}%

# Potential Loyalists: {potential_pct}%

# At Risk Customers: {risk_pct}%

# Estimated Revenue at Risk: ${risk_revenue:,.2f}

# Recommendation: Focus on converting Potential Loyalists and retaining At Risk customers.
# """)

#     # ----------------------------------
#     # DISTRIBUTION CHARTS
#     # ----------------------------------
#     st.markdown("## 📈 Customer Distribution")

#     category_counts = analysis_df["Customer Category"].value_counts()

#     col1, col2 = st.columns(2)

#     with col1:
#         st.bar_chart(category_counts)

#     with col2:
#         fig = px.pie(
#             names=category_counts.index,
#             values=category_counts.values,
#             title="Customer Segments"
#         )
#         st.plotly_chart(fig, use_container_width=True)

#     # ----------------------------------
#     # TOP CUSTOMERS
#     # ----------------------------------
#     st.markdown("## 🏆 Top Customers")

#     st.dataframe(
#         analysis_df.sort_values("Loyalty Score", ascending=False).head(10),
#         use_container_width=True
#     )

#     # ----------------------------------
#     # 🔍 CUSTOMER SEARCH (FULL RESTORED PROFILE)
#     # ----------------------------------
#     st.markdown("## 🔍 Customer Profile Search")

#     search_id = st.text_input("Enter Customer ID")

#     if search_id:
#         result = analysis_df[
#             analysis_df[customer_id_col].astype(str) == search_id
#         ]

#         if not result.empty:
#             st.success("Customer Found")

#             customer = result.iloc[0]

#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.metric("Customer ID", str(customer[customer_id_col]))

#             with col2:
#                 st.metric("Loyalty Score", int(customer["Loyalty Score"]))

#             with col3:
#                 st.metric("Category", customer["Customer Category"])

#             st.markdown("### 🧠 Recommended Action")

#             if customer["Customer Category"] == "Loyal Customer":
#                 st.success("Offer VIP rewards + referral program")
#             elif customer["Customer Category"] == "Potential Loyalist":
#                 st.info("Run personalized engagement campaigns")
#             else:
#                 st.warning("Immediate retention campaign required")
#         else:
#             st.warning("Customer not found")

#     # ----------------------------------
#     # DOWNLOAD
#     # ----------------------------------
#     st.markdown("## ⬇ Export Data")

#     csv = analysis_df.to_csv(index=False)

#     st.download_button(
#         "Download Analysis CSV",
#         csv,
#         "loyallens_analysis.csv",
#         "text/csv"
#     )
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# CONFIG
# ----------------------------------
st.set_page_config(
    page_title="LoyalLens AI",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------------
# PREMIUM SaaS THEME (PITCH READY)
# ----------------------------------
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1220, #070a12);
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 2.2rem 3rem;
}

/* Hero feel */
.hero {
    padding: 1.5rem 0;
}

/* Headings */
h1, h2, h3 {
    color: white;
    font-weight: 650;
    letter-spacing: 0.2px;
}

/* Metrics (investor cards) */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    transform: translateY(-2px);
}

/* Inputs */
input, textarea, select {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HERO SECTION (PITCH STYLE)
# ----------------------------------
st.markdown("""
<div class="hero">
<h1>🚀 LoyalLens AI</h1>
<h3>Customer Retention & Revenue Intelligence Platform</h3>
<p style="color:rgba(255,255,255,0.65)">
Turn customer data into revenue strategy. Predict churn. Maximize lifetime value. Increase retention automatically.
</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# FILE UPLOAD (ENTRY POINT)
# ----------------------------------
uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.success("AI Engine Activated — Dataset Loaded")

    columns = list(df.columns)

    # ----------------------------------
    # COLUMN MAPPING (SIMPLIFIED LIKE SAAS TOOL)
    # ----------------------------------
    st.markdown("## ⚙️ AI Data Mapping Engine")

    customer_id_col = st.selectbox("Customer ID", columns)
    order_value_col = st.selectbox("Order Value", columns)
    discount_col = st.selectbox("Discount (Optional)", ["Not Available"] + columns)

    # ----------------------------------
    # AI LOYALTY ENGINE
    # ----------------------------------
    analysis_df = df.copy()

    max_value = analysis_df[order_value_col].max()

    analysis_df["Loyalty Score"] = (
        analysis_df[order_value_col] / max_value * 100
        if max_value > 0 else 0
    )

    if discount_col != "Not Available":
        max_discount = analysis_df[discount_col].max()
        if max_discount > 0:
            discount_score = (1 - analysis_df[discount_col] / max_discount) * 30
            analysis_df["Loyalty Score"] = (
                analysis_df["Loyalty Score"] * 0.7 + discount_score
            )

    analysis_df["Loyalty Score"] = analysis_df["Loyalty Score"].clip(0, 100)

    def classify(x):
        if x >= 80:
            return "High Value Customer"
        elif x >= 50:
            return "Growth Potential"
        return "Churn Risk"

    analysis_df["Customer Segment"] = analysis_df["Loyalty Score"].apply(classify)

    # ----------------------------------
    # KPI STRIP (INVESTOR STYLE)
    # ----------------------------------
    st.markdown("## 📊 Executive Growth Overview")

    total = len(analysis_df)
    high = len(analysis_df[analysis_df["Customer Segment"] == "High Value Customer"])
    growth = len(analysis_df[analysis_df["Customer Segment"] == "Growth Potential"])
    risk = len(analysis_df[analysis_df["Customer Segment"] == "Churn Risk"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers", total)
    c2.metric("High Value", high)
    c3.metric("Growth Potential", growth)
    c4.metric("Churn Risk", risk)

    # ----------------------------------
    # INSIGHT ENGINE (MARKET-READY LANGUAGE)
    # ----------------------------------
    st.markdown("## 🧠 AI Insight Engine")

    high_pct = round((high / total) * 100, 1)
    growth_pct = round((growth / total) * 100, 1)
    risk_pct = round((risk / total) * 100, 1)

    st.write(f"🟢 High Value Customers: {high_pct}%")
    st.write(f"🟡 Growth Potential Customers: {growth_pct}%")
    st.write(f"🔴 Churn Risk Customers: {risk_pct}%")

    if risk_pct > 50:
        st.error("⚠️ Critical: High churn exposure detected across customer base.")
    elif high_pct > 50:
        st.success("💎 Strong retention moat — high LTV customer base.")
    else:
        st.info("📊 Balanced customer structure with scaling opportunity.")

    # ----------------------------------
    # REVENUE FORECAST MODULE (PITCH STYLE)
    # ----------------------------------
    st.markdown("## 💰 Revenue Intelligence & Forecast")

    total_revenue = df[order_value_col].sum()
    avg_order = df[order_value_col].mean()
    risk_revenue = risk * avg_order

    col1, col2 = st.columns(2)
    col1.success(f"Total Revenue Generated: ${total_revenue:,.2f}")
    col2.error(f"Forecasted Revenue at Risk: ${risk_revenue:,.2f}")

    st.caption("AI-based estimation using customer segmentation model")

    # ----------------------------------
    # VISUAL MARKET DASHBOARD
    # ----------------------------------
    st.markdown("## 📈 Market Distribution View")

    counts = analysis_df["Customer Segment"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(counts)

    with col2:
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Customer Market Segments"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------
    # CUSTOMER INTELLIGENCE PANEL
    # ----------------------------------
    st.markdown("## 🔍 Customer Intelligence Panel")

    search_id = st.text_input("Search Customer ID")

    if search_id:
        result = analysis_df[
            analysis_df[customer_id_col].astype(str) == search_id
        ]

        if not result.empty:
            c = result.iloc[0]

            c1, c2, c3 = st.columns(3)
            c1.metric("Customer ID", str(c[customer_id_col]))
            c2.metric("Loyalty Score", int(c["Loyalty Score"]))
            c3.metric("Segment", c["Customer Segment"])

            st.markdown("### 🤖 AI Recommendation")

            if c["Customer Segment"] == "High Value Customer":
                st.success("Retain with VIP perks + loyalty programs")
            elif c["Customer Segment"] == "Growth Potential":
                st.info("Upsell campaigns recommended")
            else:
                st.warning("Immediate retention intervention required")

        else:
            st.warning("Customer not found")

    # ----------------------------------
    # EXPORT (INVESTOR REPORT)
    # ----------------------------------
    st.markdown("## 📁 Export Investor Report")

    csv = analysis_df.to_csv(index=False)

    st.download_button(
        "Download Full AI Report",
        csv,
        "loyallens_investor_grade_report.csv",
        "text/csv"
    )
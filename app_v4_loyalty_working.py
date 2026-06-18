import streamlit as st
import pandas as pd

# ----------------------------------

# PAGE CONFIGURATION

# ----------------------------------

st.set_page_config(
page_title="LoyalLens",
layout="wide"
)

# ----------------------------------

# TITLE

# ----------------------------------

st.title("🚀 LoyalLens")
st.subheader("Know who loves your brand and who loves your discounts")

# ----------------------------------

# FILE UPLOAD

# ----------------------------------

uploaded_file = st.file_uploader(
"Upload your customer CSV file",
type=["csv"]
)

# ----------------------------------

# PROCESS FILE

# ----------------------------------

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully!")

    # ----------------------------------
    # DATA PREVIEW
    # ----------------------------------

    st.write("## 📊 Data Preview")
    st.dataframe(df.head())

    # ----------------------------------
    # AVAILABLE COLUMNS
    # ----------------------------------

    columns = list(df.columns)

    st.write("## 📋 Available Columns")
    st.write(columns)

    # ----------------------------------
    # SMART COLUMN DETECTION
    # ----------------------------------

    customer_id_guess = next(
        (col for col in columns if "id" in col.lower()),
        columns[0]
    )

    order_value_guess = next(
        (
            col for col in columns
            if "value" in col.lower()
            or "amount" in col.lower()
            or "revenue" in col.lower()
            or "sales" in col.lower()
        ),
        columns[0]
    )

    discount_guess = next(
        (
            col for col in columns
            if "discount" in col.lower()
        ),
        None
    )

    # ----------------------------------
    # COLUMN MAPPING
    # ----------------------------------

    st.write("## 🤖 Confirm Column Mapping")

    customer_id_col = st.selectbox(
        "Customer ID Column",
        columns,
        index=columns.index(customer_id_guess)
    )

    order_value_col = st.selectbox(
        "Order Value Column",
        columns,
        index=columns.index(order_value_guess)
    )

    discount_col = st.selectbox(
        "Discount Column (Optional)",
        ["Not Available"] + columns,
        index=0
    )

    customer_name_col = st.selectbox(
        "Customer Name Column (Optional)",
        ["Not Available"] + columns,
        index=0
    )

    order_date_col = st.selectbox(
        "Order Date Column (Optional)",
        ["Not Available"] + columns,
        index=0
    )

    st.success("Column mapping completed!")

    # ----------------------------------
    # MAPPING SUMMARY
    # ----------------------------------

    st.write("## ✅ Mapping Summary")

    st.write(f"Customer ID → {customer_id_col}")
    st.write(f"Order Value → {order_value_col}")
    st.write(f"Discount → {discount_col}")
    st.write(f"Customer Name → {customer_name_col}")
    st.write(f"Order Date → {order_date_col}")
        # ----------------------------------
    # FLEXIBLE LOYALTY ANALYSIS
    # ----------------------------------

    st.write("## 📈 Loyalty Analysis")

    analysis_df = df.copy()

    # Create Loyalty Score from Order Value

    max_value = analysis_df[order_value_col].max()

    if max_value > 0:
        analysis_df["Loyalty Score"] = (
            analysis_df[order_value_col] / max_value
        ) * 100
    else:
        analysis_df["Loyalty Score"] = 0

    # If discount column exists,
    # reward customers who buy with fewer discounts

    if discount_col != "Not Available":

        max_discount = analysis_df[discount_col].max()

        if max_discount > 0:

            discount_score = (
                1 -
                (
                    analysis_df[discount_col]
                    / max_discount
                )
            ) * 30

            analysis_df["Loyalty Score"] = (
                analysis_df["Loyalty Score"] * 0.7
                + discount_score
            )

    analysis_df["Loyalty Score"] = (
        analysis_df["Loyalty Score"]
        .clip(0, 100)
        .round(0)
    )

    # Customer Category

    def categorize(score):

        if score >= 80:
            return "Loyal Customer"

        elif score >= 50:
            return "Potential Loyalist"

        else:
            return "At Risk"

    analysis_df["Customer Category"] = (
        analysis_df["Loyalty Score"]
        .apply(categorize)
    )

    # Results Table

    st.write("## 📋 Analysis Results")

    st.dataframe(
        analysis_df[
            [
                customer_id_col,
                "Loyalty Score",
                "Customer Category"
            ]
        ].head(20)
    )

    # Dashboard

    st.write("## 📊 Customer Segment Dashboard")

    total_customers = len(analysis_df)

    loyal_count = len(
        analysis_df[
            analysis_df["Customer Category"]
            == "Loyal Customer"
        ]
    )

    potential_count = len(
        analysis_df[
            analysis_df["Customer Category"]
            == "Potential Loyalist"
        ]
    )

    risk_count = len(
        analysis_df[
            analysis_df["Customer Category"]
            == "At Risk"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Customers",
            total_customers
        )

    with col2:
        st.metric(
            "Loyal Customers",
            loyal_count
        )

    with col3:
        st.metric(
            "Potential Loyalists",
            potential_count
        )

    with col4:
        st.metric(
            "At Risk",
            risk_count
        )

    # Chart

    st.write("## 📈 Customer Category Distribution")

    st.bar_chart(
        analysis_df["Customer Category"]
        .value_counts()
    )

    # Top Customers

    st.write("## 🏆 Top 10 Loyal Customers")

    top_customers = (
        analysis_df
        .sort_values(
            by="Loyalty Score",
            ascending=False
        )
    )

    st.dataframe(
        top_customers[
            [
                customer_id_col,
                "Loyalty Score",
                "Customer Category"
            ]
        ].head(10)
    )

    # Download

    st.write("## ⬇ Download Analysis")

    csv = analysis_df.to_csv(index=False)

    st.download_button(
        label="Download Analysis CSV",
        data=csv,
        file_name="loyallens_analysis.csv",
        mime="text/csv"
    )

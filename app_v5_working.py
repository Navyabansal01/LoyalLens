import streamlit as st
import pandas as pd
import plotly.express as px

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
st.markdown(
    "### AI-Powered Customer Loyalty Intelligence Platform"
)
st.markdown(
    "Analyze customer behavior, identify loyal customers, and uncover retention opportunities."
)
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

    
        # ----------------------------------
    # BUSINESS INSIGHTS
    # ----------------------------------

    st.write("## 📌 Key Insights")

    loyal_pct = round(
        (loyal_count / total_customers) * 100,
        1
    )

    potential_pct = round(
        (potential_count / total_customers) * 100,
        1
    )

    risk_pct = round(
        (risk_count / total_customers) * 100,
        1
    )

    st.write(
        f"🟢 {loyal_pct}% customers are Loyal Customers"
    )

    st.write(
        f"🟡 {potential_pct}% customers are Potential Loyalists"
    )

    st.write(
        f"🔴 {risk_pct}% customers are At Risk"
    )

    if risk_pct > 50:
        st.warning(
            "More than half of customers are At Risk. Retention strategies are recommended."
        )

    elif loyal_pct > 50:
        st.success(
            "Excellent customer loyalty. A majority of customers are highly engaged."
        )

    else:
        st.info(
            "Customer loyalty is balanced, with opportunities for growth."
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
            loyal_count,
            f"{loyal_pct}%"
        )

    with col3:
        st.metric(
            "Potential Loyalists",
            potential_count,
            f"{potential_pct}%"
        )

    with col4:
        st.metric(
            "At Risk",
            risk_count,
            f"{risk_pct}%"
        )

    # Chart

    # st.write("## 📈 Customer Category Distribution")

    # st.bar_chart(
    #     analysis_df["Customer Category"]
    #     .value_counts()
    # )
    st.write("## 📈 Customer Category Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Bar Chart")
        st.bar_chart(
            analysis_df["Customer Category"]
            .value_counts()
        )

    with col2:
        st.write("### Distribution Table")

        category_counts = (
            analysis_df["Customer Category"]
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Customer Category",
            "Count"
        ]

        st.dataframe(
            category_counts,
            use_container_width=True
        )
        st.write("### 🥧 Customer Distribution Pie Chart")

    fig = px.pie(
        category_counts,
        names="Customer Category",
        values="Count",
        title="Customer Segment Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

        # Top Customers

    st.divider()
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
        # ----------------------------------
    # CUSTOMER SEARCH
    # ----------------------------------
 
    st.divider()
    st.write("## 🔍 Customer Search")

    search_id = st.text_input(
        "Enter Customer ID"
    )

    if search_id:

        result = analysis_df[
            analysis_df[customer_id_col]
            .astype(str)
            == search_id
        ]

        if len(result) > 0:

            st.success("Customer Found")

            st.dataframe(
                result[
                    [
                        customer_id_col,
                        "Loyalty Score",
                        "Customer Category"
                    ]
                ]
            )

        else:

            st.warning(
                "Customer ID not found"
            )

    # Download

    st.divider()
    st.write("## ⬇ Download Analysis")

    csv = analysis_df.to_csv(index=False)

    st.download_button(
        label="Download Analysis CSV",
        data=csv,
        file_name="loyallens_analysis.csv",
        mime="text/csv"
    )

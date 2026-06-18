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


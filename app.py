import streamlit as st

st.set_page_config(page_title="LoyalLens", layout="wide")

st.title("🚀 LoyalLens")
st.subheader("Know who loves your brand and who loves your discounts")

uploaded_file = st.file_uploader(
    "Upload your customer CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.write("Filename:", uploaded_file.name)

import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

@st.cache_data
def train_models(df):
    product_models = {}
    unique_products = df['Product_ID'].unique()
    for product_id in unique_products:
        product_df = df[df['Product_ID'] == product_id].copy()
        if len(product_df) < 5:
            continue
        product_df['month'] = product_df['Date'].dt.month
        product_df['day_of_week'] = product_df['Date'].dt.dayofweek
        features = product_df[['Price', 'month', 'day_of_week']]
        model = IsolationForest(contamination='auto', random_state=42)
        model.fit(features)
        product_models[product_id] = model
    return product_models

st.title("🛒 Fake Discount Detector [Anomaly Detection Demo]")
st.markdown("""
Upload your product price time series Excel file and test if a product price on a particular date is **inflated** (anomaly).
""")

data_file = st.file_uploader("Upload updated_product_price_timeseries.xlsx", type=["xlsx"])
if data_file:
    df = pd.read_excel(data_file)
    df['Date'] = pd.to_datetime(df['Date'])
    st.success("Data loaded! Training specialized models per product...")
    product_models = train_models(df)
    st.success(f"Models trained for {len(product_models)} products.")

    st.header("🔎 Detect Anomaly for Product Price")
    product_id = st.selectbox("Select Product ID", options=df['Product_ID'].unique())
    price = st.number_input("Enter price", min_value=0.0)
    date_str = st.text_input("Date (YYYY-MM-DD)", value=str(df['Date'].max().date()))
    if st.button("Detect Anomaly"):
        if product_id in product_models:
            try:
                date_obj = pd.to_datetime(date_str)
                month = date_obj.month
                day_of_week = date_obj.dayofweek
                input_data = np.array([[price, month, day_of_week]])
                model = product_models[product_id]
                prediction = model.predict(input_data)[0]
                anomaly_score = model.score_samples(input_data)[0]
                if prediction == -1:
                    st.error(f"🔴 Inflated (Anomaly Score: {anomaly_score:.3f}) — Possible fake discount!!")
                else:
                    st.success(f"🟢 Not Inflated (Anomaly Score: {anomaly_score:.3f})")
            except Exception as ex:
                st.warning("Invalid date format or input. Use YYYY-MM-DD.")
        else:
            st.warning("Unknown Product ID.")
    st.subheader("Preview Data")
    st.dataframe(df)
else:
    st.info("Awaiting Excel file upload...")

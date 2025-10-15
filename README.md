# Fake Discount Detector (Streamlit App)

Detect fake/inflated product prices using anomaly detection with Isolation Forest.

## Usage

1. Upload your Excel dataset (`updated_product_price_timeseries.xlsx`) in the app.
2. Choose a product, price, and date to check if the price is anomalously high (fake discount).
3. See the result instantly!

## Dataset Format

- **Product_ID** (string)
- **Price** (float)
- **Date** (YYYY-MM-DD)

Sample:

| Product_ID | Price | Date       |
|------------|-------|------------|
| P0022      | 299   | 2024-08-01 |
| P0022      | 285   | 2024-08-08 |
| P0033      | 999   | 2024-07-25 |

## Local run


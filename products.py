import streamlit as st
import pandas as pd
from db import get_db_conn


def display_products():
    # Function to fetch products from the database and display them
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    conn.close()

    # Define columns for DataFrame
    columns = [
        "Product Name",
        "Product Link",
        "Product Image",
        "Current Price",
        "Original Price"
    ]

    # Create DataFrame from fetched data
    products_df = pd.DataFrame(rows, columns=columns)

    # Display product image, name, and current price in the same row
    for index, row in products_df.iterrows():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image(row["Product Image"], width=100)
        with col2:
            st.write(f"**{row['Product Name']}**")
        with col3:
            st.write(f"$ {row['Current Price']}")
        st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    display_products()

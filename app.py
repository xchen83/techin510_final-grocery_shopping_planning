import streamlit as st
from products import display_products
from todo import todo_list
from inventory import track_inventory

import pandas as pd
import altair as alt


# Set page configuration
st.set_page_config(layout="wide")

# Create columns for the sidebar and main content
sidebar, main = st.columns([1, 3], gap="medium")

# Sidebar content
# Define the navigation structure
pages = {
    "🛒 Fresh Food on Walmart.com": "Fresh Food on Walmart.com",
    "📝 Grocery Planning List": "Grocery Planning List",
    "📦 Track Fridge Inventory": "Track Fridge Inventory",
    "🏦 Purchasing Insights": "Purchasing Insights"
}

# Sidebar for navigation
st.sidebar.title("Welcome Back!")
selection = st.sidebar.radio("", list(pages.keys()))

# Display the database table on the Grocery Planning List page
if selection == "🛒 Fresh Food on Walmart.com":
    st.title("🛒 Fresh Food on Walmart.com")
    st.markdown("#### Checkout the latest fresh food products on Walmart.com")
    display_products()

elif selection == "📝 Grocery Planning List":
    st.title("📝 Grocery Planning List")
    st.markdown("#### Add your food items in the list")
    todo_list()

elif selection == "📦 Track Fridge Inventory":
    st.title("📦 Track Fridge Inventory")
    st.markdown("#### Add new item to your fridge inventory")
    track_inventory()


elif selection == "🏦 Purchasing Insights":
    st.title("🏦 Purchasing Insights")
    st.markdown("#### Here are some insights from the Walmart food grocery")
    # Load the data
    file_path = 'data/products.csv'
    df = pd.read_csv(file_path)

    # Visualization 1: Bar chart for top 10 products by current price
    top_10_current_price = df.nlargest(10, 'Current Price')
    chart1 = alt.Chart(top_10_current_price).mark_bar().encode(
        x='Current Price:Q',
        y='Product Name:N',
        color='Product Name:N',
        tooltip=['Product Name', 'Current Price']
    ).properties(
        title='Table 1 - Top 10 Products by Current Price'
    )

    # Visualization 2: Histogram for distribution of original prices
    chart2 = alt.Chart(df).mark_bar().encode(
        alt.X('Original Price:Q', bin=True),
        y='count()',
        tooltip='count()'
    ).properties(
        title='Table 2 - Distribution of Original Prices'
    )

    # Visualization 3: Scatter plot for current price vs original price
    chart3 = alt.Chart(df).mark_circle().encode(
        x='Original Price:Q',
        y='Current Price:Q',
        tooltip=['Product Name', 'Original Price', 'Current Price']
    ).properties(
        title='Table 3 - Current Price vs Original Price'
    )

    vertical_concatenated_chart = alt.vconcat(chart1, chart2, chart3)
    vertical_concatenated_chart

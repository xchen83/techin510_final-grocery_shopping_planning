import streamlit as st
import sqlite3
from datetime import datetime

# Establish a connection to your SQLite database
con = sqlite3.connect("inventory.db", check_same_thread=False)  # Ensure thread safety for Streamlit
cur = con.cursor()

# Function to initialize the database
def init_db():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_date DATETIME NOT NULL,
            expiration_date DATETIME NOT NULL
        )
    ''')
    con.commit()

# Function to add an item to the inventory
def add_to_inventory(item_name, quantity, purchase_date, expiration_date):
    # Convert dates to strings in 'YYYY-MM-DD' format for SQLite
    purchase_date_str = purchase_date.strftime('%Y-%m-%d')
    expiration_date_str = expiration_date.strftime('%Y-%m-%d')

    cur.execute("INSERT INTO inventory (item_name, quantity, purchase_date, expiration_date) VALUES (?, ?, ?, ?)",
                (item_name, quantity, purchase_date_str, expiration_date_str))
    con.commit()

# Function to remove an item from the inventory
def remove_from_inventory(item_id):
    cur.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    con.commit()

# Function to list inventory items
def list_inventory():
    inventory_items = cur.execute("SELECT * FROM inventory").fetchall()
    return inventory_items

# UI function for inventory tracking in Streamlit
def track_inventory():
    with st.form("Add Item Form"):
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1, value=1)
        purchase_date = st.date_input("Purchase Date", datetime.today())
        expiration_date = st.date_input("Expiration Date")
        submit_button = st.form_submit_button(label="Add to Inventory")
        if submit_button:
            add_to_inventory(item_name, quantity, purchase_date, expiration_date)
            st.success(f"Added {quantity} of {item_name} to the inventory with expiration date on {expiration_date}.")

    # Always display the inventory list
    st.subheader("Inventory List")
    inventory_items = list_inventory()
    if inventory_items:
        for item in inventory_items:
            row = f"{item[1]} - {item[2]} units (Purchased: {item[3]}, Expires: {item[4]})"
            col1, col2 = st.columns([4, 1])  # Adjust column widths as needed
            col1.write(row)
            remove_button = col2.button(f"Remove", key=f"remove_{item[0]}")
            if remove_button:
                remove_from_inventory(item[0])
                st.experimental_rerun()  # Rerun the app to update the inventory list
    else:
        st.write("The inventory is currently empty.")

# Ensure the database is initialized when this module is imported
init_db()

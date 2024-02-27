import sqlite3
import streamlit as st

# Connect to your SQLite database
con = sqlite3.connect("groceryshoppingapp.sqlite", isolation_level=None)
cur = con.cursor()


# Function to fetch checked items from the database
def fetch_checked_items():
    checked_items = cur.execute(
        "SELECT id, item, quantity FROM products WHERE status = 'purchased'"
        ).fetchall()
    return checked_items


# Function to update the status of an item
def update_item_status(item_id, status):
    cur.execute(
        "UPDATE products SET status = ? WHERE id = ?", (status, item_id)
        )
    con.commit()


# Function to display the fridge items
def fridge_items():
    # Fetch checked items
    checked_items = fetch_checked_items()

    # Display checked items with a toggle section for each item
    if checked_items:
        for item_id, item, quantity in checked_items:
            consume = st.checkbox(f" {item} x {quantity}", value=False)
            if consume:
                update_item_status(item_id, 'consumed')
                st.success(f"{item} x {quantity} has been consumed!")
    else:
        st.write("Your fridge is empty!", font="Helvetica")


if __name__ == "__main__":
    fridge_items()

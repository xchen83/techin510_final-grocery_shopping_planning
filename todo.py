import sqlite3
from datetime import datetime
from enum import Enum

import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp

# Function to create a new database connection
def get_db_connection():
    return sqlite3.connect("groceryshoppingapp.sqlite", isolation_level=None)

# Function to create the table if it doesn't exist
def create_products_table():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            item TEXT NOT NULL,
            quantity INT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
        """
    )
    con.close()

class TaskStatus(str, Enum):
    planned = "planned"
    purchased = "purchased"

class Task(BaseModel):
    item: str
    quantity: int
    price: float
    status: TaskStatus = TaskStatus.planned

# Toggle task status
def toggle_status(task_id, new_status):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("UPDATE products SET status = ? WHERE id = ?", (new_status, task_id))
    con.close()

# Delete a task
def delete_task(task_id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (task_id,))
    con.close()

# Fetch all products from the database
def fetch_all_products_from_db():
    con = get_db_connection()
    cur = con.cursor()
    products = cur.execute("SELECT * FROM products").fetchall()
    con.close()
    return products

def todo_list():
    create_products_table()  # Ensure the table exists

    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO products (item, quantity, price, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data.item, data.quantity, data.price, data.status.value, datetime.now()),
        )
        con.close()
        st.success("Product added successfully!")

    products = fetch_all_products_from_db()

    header_cols = st.columns([1, 3, 2, 2, 2, 2])  # Add an extra column for total price
    header_cols[0].write("Status")
    header_cols[1].write("Item")
    header_cols[2].write("Quantity")
    header_cols[3].write("Price")
    header_cols[4].write("Total Price")  # Header for total price
    header_cols[5].write("Actions")

    grand_total = 0  # Initialize grand total

    for task in products:
        task_cols = st.columns([1, 3, 2, 2, 2, 2])  # Adjust for the additional total price column
        current_status = task[4]
        is_purchased = current_status == 'purchased'
        if task_cols[0].checkbox("", value=is_purchased, key=f"status_{task[0]}"):
            new_status = 'purchased' if not is_purchased else 'planned'
            toggle_status(task[0], new_status)
            st.experimental_rerun()

        task_cols[1].write(task[1])
        task_cols[2].write(task[2])
        task_cols[3].write(task[3])
        total_price = task[2] * task[3]  # Calculate total price for this item
        task_cols[4].write(f"{total_price:.2f}")  # Display total price

        grand_total += total_price  # Add to grand total

        if task_cols[5].button("Delete", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.experimental_rerun()

    # Display grand total
    st.write(f"Grand Total: {grand_total:.2f}")

if __name__ == "__main__":
    todo_list()

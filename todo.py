import sqlite3
from datetime import datetime
from enum import Enum

import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp

# Connect to our database
con = sqlite3.connect("groceryshoppingapp.sqlite", isolation_level=None)
cur = con.cursor()

# Create the table with 'status'
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
    cur.execute(
        "UPDATE products SET status = ? WHERE id = ?", (new_status, task_id)
        )


# Delete a task
def delete_task(task_id):
    cur.execute("DELETE FROM products WHERE id = ?", (task_id,))


def fetch_all_products_from_db():
    return cur.execute("SELECT * FROM products").fetchall()


def todo_list():

    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        cur.execute(
            """
            INSERT INTO products (item, quantity, price, status, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data.item, data.quantity, data.price, data.status.value,
             datetime.now()),
        )
        st.success("Product added successfully!")

    # Fetch all products from database
    products = fetch_all_products_from_db()

    # Create a header row
    header_cols = st.columns([1, 3, 2, 2, 2])
    header_cols[0].write("Status")
    header_cols[1].write("Item")
    header_cols[2].write("Quantity")
    header_cols[3].write("Price")
    header_cols[4].write("Actions")

    for task in products:
        task_cols = st.columns([1, 3, 2, 2, 2])

        # Checkbox to toggle task status
        current_status = task[4]
        is_purchased = current_status == 'purchased'
        if task_cols[0].checkbox(
            "", value=is_purchased, key=f"status_{task[0]}"
        ):
            if not is_purchased:
                toggle_status(task[0], 'purchased')
        elif is_purchased:
            toggle_status(task[0], 'planned')

        # Display task item, quantity, price
        task_cols[1].write(task[1])
        task_cols[2].write(task[2])
        task_cols[3].write(task[3])

        # Edit button for each task
        if task_cols[4].button("Delete", key=f"delete_{task[0]}"):
            delete_task(task[0])
            st.experimental_rerun()


if __name__ == "__main__":
    todo_list()

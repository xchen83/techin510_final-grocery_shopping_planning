import csv
from db import get_db_conn


def create_table():
    # Define the SQL command to create the table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS products (
        product_name TEXT,
        product_link TEXT,
        product_image TEXT,
        current_price NUMERIC,
        original_price NUMERIC
    );
    '''

    # Establish a connection to the database
    conn = get_db_conn()

    # Create a cursor object
    cur = conn.cursor()

    # Execute the SQL command to create the table
    cur.execute(create_table_query)

    # Close the cursor and connection
    cur.close()
    conn.close()


def update_database():
    # Create the table if it doesn't exist
    create_table()

    # Establish a connection to the database
    conn = get_db_conn()

    # Create a cursor object
    cur = conn.cursor()

    # Open the CSV file and insert its contents into the database
    with open('data/products.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            for i in range(len(row)):
                if row[i] == "":
                    row[i] = None

            print("Row to be inserted:", row)
            if len(row) != 5:
                print("Error: Row does not contain exactly five columns")
                continue

            # Insert the row into the database
            cur.execute(
                "INSERT INTO products (product_name, product_link,product_image, current_price, original_price) VALUES (%s, %s, %s, %s, %s)",
                row
            )

    conn.commit()
    cur.close()
    conn.close()

    print("Database update complete.")


if __name__ == "__main__":
    update_database()

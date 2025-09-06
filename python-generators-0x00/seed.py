import mysql.connector
from mysql.connector import errorcode
import uuid
import csv


def connect_db():
    """Connect to MySQL server (not to a specific database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",   # change if needed
            user="root",        # your MySQL username
            password="xyzxyz" # your MySQL password
        )
        print("Connected to MySQL server")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ready")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="xyzxyz",
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(table_query)
        print("user_data table ready")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    cursor.close()


def insert_data(connection, data):
    """Insert data into user_data if not already exists."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    SELECT %s, %s, %s, %s
    FROM DUAL
    WHERE NOT EXISTS (
        SELECT 1 FROM user_data WHERE email = %s
    )
    """
    try:
        for row in data:
            user_id = str(uuid.uuid4())  # generate UUID
            cursor.execute(insert_query, (user_id, row["name"], row["email"], row["age"], row["email"]))
        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    cursor.close()


def load_csv_data(filename):
    """Load user data from CSV file."""
    data = []
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({
                    "name": row["name"],
                    "email": row["email"],
                    "age": row["age"]
                })
        print("CSV data loaded")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return data


if __name__ == "__main__":
    # Step 1: Connecting to MySQL server
    conn = connect_db()
    if conn:
        # Step 2: Createing database
        create_database(conn)
        conn.close()

        # Step 3: Connecting to ALX_prodev
        conn_prodev = connect_to_prodev()
        if conn_prodev:
            # Step 4: Creating table
            create_table(conn_prodev)

            # Step 5: Load CSV data
            data = load_csv_data("user_data.csv")

            # Step 6: Insert data
            insert_data(conn_prodev, data)

            conn_prodev.close()

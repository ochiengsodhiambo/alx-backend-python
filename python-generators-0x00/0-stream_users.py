import mysql.connector

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # change to your MySQL username
        password="xyzxyz",  # change to your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:   # only one loop
        yield row

    cursor.close()
    connection.close()


# Example usage:
if __name__ == "__main__":
    for user in stream_users():
        print(user)

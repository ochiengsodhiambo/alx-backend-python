import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from the user_data table in batches.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # change to your MySQL username
        password="xyzxyz",  # change to your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch   # yield each batch at a time

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches:
    Filters users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered = [user for user in batch if int(user["age"]) > 25]  # loop 2 (comprehension)
        yield filtered




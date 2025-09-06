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
        yield from batch   # yield rows one by one (still fetched in batches)

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches:
    Yields users over the age of 25 one by one.
    """
    for user in stream_users_in_batches(batch_size):   # loop 1
        if int(user["age"]) > 25:                      # filtering condition
            yield user                                 # yield generator


# Example usage:
if __name__ == "__main__":
    for user in batch_processing(3):   # loop 2
        print("User over 25:", user)

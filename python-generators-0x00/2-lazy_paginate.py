import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # change to your MySQL username
        password="xyzxyz",  # change to your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of users.
    """
    offset = 0
    while True:   # one loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Example usage:
if __name__ == "__main__":
    for page in lazy_paginate(2):   # fetch pages lazily
        print("Fetched page:", page)

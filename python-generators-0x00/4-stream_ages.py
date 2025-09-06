import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",          # change to your MySQL username
        password="xyzxyz",  # change to your MySQL password
        database="ALX_prodev"
    )
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:   # loop 1
        yield int(age)

    cursor.close()
    connection.close()


def compute_average_age():
    """
    Computes the average age using the generator without loading all data into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():   # loop 2
        total += age
        count += 1

    if count == 0:
        return 0
    return total / count


if __name__ == "__main__":
    avg_age = compute_average_age()
    print(f"Average age of users: {avg_age}")

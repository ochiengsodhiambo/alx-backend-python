import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results   # ✅ returns results directly when using "with"

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if exc_type is None:
                self.conn.commit()   # commit if no errors
            else:
                self.conn.rollback() # rollback if an error occurred
            self.conn.close()

# ✅ Usage: fetch users with age > 25
with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)

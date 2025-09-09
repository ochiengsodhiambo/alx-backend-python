## Overview
This project demonstrates advanced Python techniques for managing database connections and executing queries using context managers and asynchronous programming. 
It provides three key implementations: a custom context manager for database connections, a reusable query executor, and concurrent asynchronous database operations.

### 0-databaseconnection.py
A custom context manager for handling a database connection using __enter__ and __exit__.
Explanation
__enter__ → opens the connection and returns it.
__exit__ → commits changes if successful, rolls back if an exception occurred, then closes the connection.
With the with statement, you can safely run queries, and resources are always cleaned up.

### 1-execute.py
A class-based context manager ExecuteQuery that accepts a query and parameters, executes it, and returns the results inside a with block.
__init__ stores the database name, query, and parameters.
__enter__ opens the connection, executes the query with parameters, fetches results, and returns them directly.
__exit__ commits if all went well, rolls back if there was an error, then closes the connection.

###  3-concurrent.py
aiosqlite.connect() opens a database connection asynchronously.
async with db.execute(...) ensures queries run without blocking.
await cursor.fetchall() fetches results asynchronously.
asyncio.gather() runs both queries concurrently.
asyncio.run(fetch_concurrently()) kicks everything off.

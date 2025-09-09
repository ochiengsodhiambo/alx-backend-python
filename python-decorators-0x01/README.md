## Explanation
### 0-log_queries.py
The log_queries decorator wraps the target function.
It extracts the query argument from either kwargs or args.
Before calling the actual function, it prints the query for logging.
The wrapped function (fetch_all_users) then executes the query.

### 1-with_db_connection.py
with_db_connection opens the connection.
It passes conn as the first argument to your function (get_user_by_id).
The function uses that connection as if you had opened it manually.
After execution (success or error), the connection is automatically closed with finally.

### 2-transactional.py

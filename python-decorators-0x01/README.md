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
with_db_connection → opens and closes the connection.
transactional → ensures the function runs inside a transaction.
Commit if successful.
Rollback if an exception is raised.
Order matters: @with_db_connection wraps outside @transactional so that conn exists before transactions are managed.

### 3-retry_on_failure.py
with_db_connection → opens/closes the DB connection automatically.
retry_on_failure(retries, delay) → wraps the function in a retry loop.
Tries up to retries times.
Waits delay seconds before retrying if an exception occurs.
Raises the last exception if all attempts fail.

### 4-cache_query.py
query_cache is a global dictionary storing query → results.
On cache hit, the cached results are returned immediately.
On cache miss, the query executes, results are stored, then returned.
Works with both positional (args) and keyword (kwargs) query arguments.


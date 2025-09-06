## Python generators
## Seed Script 

## Overview
This repository contains a Python script (`seed.py`) that sets up a MySQL database and populates it with sample user data from a CSV file.

## Features
- Connects to a MySQL server.
- Creates a database named **ALX_prodev**.
- Connects to the **ALX_prodev** database.
- Creates a table **user_data** with the following fields:
  - `user_id` (Primary Key, UUID, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL, UNIQUE)
  - `age` (DECIMAL, NOT NULL)
- Reads data from `user_data.csv`.
- Inserts data into the database, avoiding duplicate entries based on email.

## Batch processing Large Data
stream_users_in_batches(batch_size)
  - Uses cursor.fetchmany(batch_size) → pulls rows in chunks.
  - Yields each batch.
batch_processing(batch_size)
   - Gets batches from the generator.
   - Filters users with age > 25 (list comprehension counts as 1 loop).
   - Yields filtered batch.
Loop count check:
  - for batch in stream_users_in_batches(...)
  - List comprehension for filtering.
  - The outermost usage loop (for processed_batch in batch_processing(...)).

## Lazy loading Paginated Data
paginate_users(page_size, offset) → Executes a query with LIMIT + OFFSET to simulate pagination.
lazy_paginate(page_size) → Uses a single while loop. Each iteration:
   - Calls paginate_users with the current offset.
   - Yields the page.
   - Updates offset (offset += page_size).
Stops when an empty result is returned.

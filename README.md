## alx-backend-python
# Seed Script Documentation

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


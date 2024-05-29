import sqlite3
import random
import time
from tabulate import tabulate

# Connect to SQLite databases
conn_1000 = sqlite3.connect('1000.sqlite3')
cursor_1000 = conn_1000.cursor()

conn_10000 = sqlite3.connect('10000.sqlite3')
cursor_10000 = conn_10000.cursor()

conn_100000 = sqlite3.connect('100000.sqlite3')
cursor_100000 = conn_100000.cursor()

# Function to perform search by primary key
def search_by_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        random_id = random.randint(1, 1000)  # Generate random primary key
        start_time = time.time()
        cursor.execute("SELECT * FROM myapp_workers WHERE id=?", (random_id,))
        result = cursor.fetchone()  # Retrieve worker by primary key
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return result, average_time

# Function to perform search by non-primary key field
def search_by_non_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        random_status = random.choice(['фельдшер', 'медсестра', 'водитель'])  # Generate random status
        start_time = time.time()
        cursor.execute("SELECT * FROM myapp_workers WHERE status=?", (random_status,))
        result = cursor.fetchall()  # Retrieve workers by status
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return result, average_time

# Function to perform search by mask
def search_by_mask(cursor):
    total_time = 0
    for _ in range(100):
        random_name_mask = f"%{random.choice(['a', 'e', 'i', 'o', 'u'])}%"  # Generate random name mask
        start_time = time.time()
        cursor.execute("SELECT * FROM myapp_workers WHERE name LIKE ?", (random_name_mask,))
        result = cursor.fetchall()  # Retrieve workers by name mask
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return result, average_time

# Function to add a single record
def add_single_record(cursor):
    total_time = 0
    for _ in range(100):
        start_time = time.time()
        cursor.execute("INSERT INTO myapp_workers (name, status, startwork) VALUES (?, ?, ?)", ("New Worker", "фельдшер", "2024-05-29"))
        cursor.connection.commit()
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to add a group of records
def add_group_of_records(cursor):
    total_time = 0
    for _ in range(100):
        start_time = time.time()
        for _ in range(10):  # Perform 10 times
            cursor.execute("INSERT INTO myapp_workers (name, status, startwork) VALUES (?, ?, ?)", ("New Worker", "медсестра", "2024-05-29"))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to update a record by primary key
def update_by_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        random_id = random.randint(1, 1000)  # Generate random primary key
        start_time = time.time()
        cursor.execute("UPDATE myapp_workers SET name=? WHERE id=?", ("Updated Worker", random_id))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to update a record by non-primary key field
def update_by_non_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        start_time = time.time()
        cursor.execute("UPDATE myapp_workers SET name=? WHERE status=?", ("Updated Driver", "водитель"))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to delete a record by primary key
def delete_by_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        random_id = random.randint(1, 1000)  # Generate random primary key
        start_time = time.time()
        cursor.execute("DELETE FROM myapp_workers WHERE id=?", (random_id,))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to delete a record by non-primary key field
def delete_by_non_primary_key(cursor):
    total_time = 0
    for _ in range(100):
        start_time = time.time()
        random_status = random.choice(['фельдшер', 'медсестра', 'водитель'])  # Generate random status
        cursor.execute("DELETE FROM myapp_workers WHERE status=?", (random_status,))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Function to delete a group of records
def delete_group_of_records(cursor):
    total_time = 0
    for _ in range(100):
        start_time = time.time()
        random_status = random.choice(['фельдшер', 'медсестра', 'водитель'])  # Generate random status
        cursor.execute("DELETE FROM myapp_workers WHERE status=?", (random_status,))
        cursor.connection.commit()  # Commit changes to the database
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / 100
    return average_time

# Perform operations and measure time for 1000.sqlite3
operations_1000 = {
    "Search by Primary Key": search_by_primary_key(cursor_1000),
    "Search by Non-Primary Key": search_by_non_primary_key(cursor_1000),
    "Search by Mask": search_by_mask(cursor_1000),
    "Add Single Record": add_single_record(cursor_1000),
    "Add Group of Records": add_group_of_records(cursor_1000),
    "Update by Primary Key": update_by_primary_key(cursor_1000),
    "Update by Non-Primary Key": update_by_non_primary_key(cursor_1000),
    "Delete by Primary Key": delete_by_primary_key(cursor_1000),
    "Delete by Non-Primary Key": delete_by_non_primary_key(cursor_1000),
    "Delete Group of Records": delete_group_of_records(cursor_1000)
}

# Perform operations and measure time for 10000.sqlite3
operations_10000 = {
    "Search by Primary Key": search_by_primary_key(cursor_10000),
    "Search by Non-Primary Key": search_by_non_primary_key(cursor_10000),
    "Search by Mask": search_by_mask(cursor_10000),
    "Add Single Record": add_single_record(cursor_10000),
    "Add Group of Records": add_group_of_records(cursor_10000),
    "Update by Primary Key": update_by_primary_key(cursor_10000),
    "Update by Non-Primary Key": update_by_non_primary_key(cursor_10000),
    "Delete by Primary Key": delete_by_primary_key(cursor_10000),
    "Delete by Non-Primary Key": delete_by_non_primary_key(cursor_10000),
    "Delete Group of Records": delete_group_of_records(cursor_10000)
}

# Perform operations and measure time for 100000.sqlite3
operations_100000 = {
    "Search by Primary Key": search_by_primary_key(cursor_100000),
    "Search by Non-Primary Key": search_by_non_primary_key(cursor_100000),
    "Search by Mask": search_by_mask(cursor_100000),
    "Add Single Record": add_single_record(cursor_100000),
    "Add Group of Records": add_group_of_records(cursor_100000),
    "Update by Primary Key": update_by_primary_key(cursor_100000),
    "Update by Non-Primary Key": update_by_non_primary_key(cursor_100000),
    "Delete by Primary Key": delete_by_primary_key(cursor_100000),
    "Delete by Non-Primary Key": delete_by_non_primary_key(cursor_100000),
    "Delete Group of Records": delete_group_of_records(cursor_100000)
}

# Format and print results for 1000.sqlite3
print("Results for 1000.sqlite3:")
print(tabulate(operations_1000.items(), headers=["Operation", "Average Time"], tablefmt="fancy_grid"))

# Format and print results for 10000.sqlite3
print("\nResults for 10000.sqlite3:")
print(tabulate(operations_10000.items(), headers=["Operation", "Average Time"], tablefmt="fancy_grid"))

# Format and print results for 100000.sqlite3
print("\nResults for 100000.sqlite3:")
print(tabulate(operations_100000.items(), headers=["Operation", "Average Time"], tablefmt="fancy_grid"))

# Close cursors and connections
cursor_1000.close()
conn_1000.close()

cursor_10000.close()
conn_10000.close()

cursor_100000.close()
conn_100000.close()

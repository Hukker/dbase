import sqlite3
import random
import string
import timeit
import time
from tabulate import tabulate

# Helper functions
def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return conn, c

def add_worker(c, name=None):
    worker_name = name if name else random_string()
    c.execute("INSERT INTO myapp_workers (name, status, startwork, endwork) VALUES (?, ?, ?, ?)", (worker_name, random.choice(['фельдшер', 'медсестра', 'водитель']), '2024-05-29', '2024-05-29'))
    c.connection.commit()

def add_workers_group(c, n):
    for _ in range(n):
        add_worker(c)

def find_by_key(c, id):
    c.execute("SELECT * FROM myapp_workers WHERE id = ?", (id,))
    return c.fetchone()

def find_by_non_key(c, name):
    c.execute("SELECT * FROM myapp_workers WHERE name = ?", (name,))
    return c.fetchone()

def find_by_mask(c, mask):
    c.execute("SELECT * FROM myapp_workers WHERE name LIKE ?", (mask,))
    return c.fetchall()

def update_worker_by_key(c, id):
    c.execute("UPDATE myapp_workers SET name = ? WHERE id = ?", ("TEST", id))
    c.connection.commit()

def update_worker_by_non_key(c, name):
    c.execute("UPDATE myapp_workers SET name = ? WHERE name = ?", ("TEST", name))
    c.connection.commit()

def delete_worker_by_key(c, id):
    c.execute("DELETE FROM myapp_workers WHERE id = ?", (id,))
    c.connection.commit()

def delete_worker_by_non_key(c, name):
    c.execute("DELETE FROM myapp_workers WHERE name = ?", (name,))
    c.connection.commit()

def delete_workers_group(c):
    c.execute("DELETE FROM myapp_workers WHERE status = ?", ("фельдшер",))
    c.connection.commit()

# Compression functions
def compression1(c, limit=200):

    c.execute(f"CREATE TABLE temp_table AS SELECT * FROM myapp_workers EXCEPT SELECT * FROM myapp_workers LIMIT {limit}")
    c.execute("DROP TABLE myapp_workers")
    c.execute("ALTER TABLE temp_table RENAME TO myapp_workers")
    c.execute('VACUUM')
    c.connection.commit()

def compression2(c):
    c.execute("CREATE TABLE temp_table AS SELECT * FROM myapp_workers LIMIT 200")
    c.execute("DROP TABLE myapp_workers")
    c.execute("ALTER TABLE temp_table RENAME TO myapp_workers")
    c.execute("VACUUM")
    c.connection.commit()

# Timing experiments
def measure_time(func, *args, repetitions=100):
    total_time = 0
    for _ in range(repetitions):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        total_time += end_time - start_time
    average_time = total_time / repetitions
    return average_time

def run_experiments(db_name):
    conn, c = setup_database(db_name)
    
    # Prepopulate the database with some data
    if db_name == '1000.sqlite3':
        num_records = 1000
    elif db_name == '10000.sqlite3':
        num_records = 10000
    elif db_name == '100000.sqlite3':
        num_records = 100000

    key_id = random.randint(1, num_records)  # Generate a random ID within the range of existing IDs
    specific_name = "specific_name"
    add_worker(c, specific_name)  # Add a specific worker for non-key and mask searches
    mask = '%specific%'  # Adjust to match actual data

    # Experiments
    experiments = {
        "Find by key": (find_by_key, c, key_id),
        "Find by non-key": (find_by_non_key, c, specific_name),
        "Find by mask": (find_by_mask, c, mask),
        "Add record": (add_worker, c),
        "Add group of records": (add_workers_group, c, 10),
        "Update record by key": (update_worker_by_key, c, key_id),
        "Update record by non-key": (update_worker_by_non_key, c, specific_name),
        "Delete record by key": (delete_worker_by_key, c, key_id),
        "Delete record by non-key": (delete_worker_by_non_key, c, specific_name),
        "Delete group of records": (delete_workers_group, c),
    }

    
    compression_experiments = {
        "Vacuum DB after deletion of 200 records": (compression1, c, 200),
        "Vacuum DB after leaving 200 records": (compression2, c),
    }

    results = {}
    for name, params in experiments.items():
        results[name] = measure_time(*params, repetitions=100)

    for name, params in compression_experiments.items():
        results[name] = measure_time(params[0], *params[1:], repetitions=1)

    conn.close()
    return results

# Run experiments for each database
databases = ['1000.sqlite3', '10000.sqlite3', '100000.sqlite3']
all_results = {}

for db in databases:
    all_results[db] = run_experiments(db)

# Format results
table_headers = ["Operation", "1000.sqlite3", "10000.sqlite3", "100000.sqlite3"]
table_data = []

operations = list(all_results['1000.sqlite3'].keys())
for operation in operations:
    row = [operation]
    for db in databases:
        row.append(f"{all_results[db][operation]:.6f}")
    table_data.append(row)

print(tabulate(table_data, headers=table_headers, tablefmt='grid'))

import sqlite3
import random
import string
import timeit

# Helper functions
def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def setup_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS WorkersInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            startwork DATE NOT NULL
        )
    ''')
    conn.commit()

    c.execute('''
        CREATE TABLE IF NOT EXISTS Workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            info_id INTEGER NOT NULL,
            FOREIGN KEY (info_id) REFERENCES WorkersInfo (id)
        )
    ''')
    conn.commit()
    
    return conn, c

def add_worker(c):
    c.execute("INSERT INTO WorkersInfo (startwork) VALUES (date('now'))")
    info_id = c.lastrowid
    c.execute("INSERT INTO Workers (name, status, info_id) VALUES (?, ?, ?)", (random_string(), random.choice(['фельдшер', 'медсестра', 'водитель']), info_id))
    c.connection.commit()

def add_workers_group(c, n):
    for _ in range(n):
        add_worker(c)

def find_by_key(c, id):
    c.execute("SELECT * FROM Workers WHERE id = ?", (id,))
    return c.fetchone()

def find_by_non_key(c, name):
    c.execute("SELECT * FROM Workers WHERE name = ?", (name,))
    return c.fetchone()

def find_by_mask(c, mask):
    c.execute("SELECT * FROM Workers WHERE name LIKE ?", (mask,))
    return c.fetchall()

def update_worker_by_key(c, id):
    c.execute("UPDATE Workers SET name = ? WHERE id = ?", (random_string(), id))
    c.connection.commit()

def update_worker_by_non_key(c, name):
    c.execute("UPDATE Workers SET name = ? WHERE name = ?", (random_string(), name))
    c.connection.commit()

def delete_worker_by_key(c, id):
    c.execute("DELETE FROM Workers WHERE id = ?", (id,))
    c.connection.commit()

def delete_worker_by_non_key(c, name):
    c.execute("DELETE FROM Workers WHERE name = ?", (name,))
    c.connection.commit()

def delete_workers_group(c, n):
    c.execute("DELETE FROM Workers WHERE id IN (SELECT id FROM Workers LIMIT ?)", (n,))
    c.connection.commit()

def vacuum_db(c):
    c.execute("VACUUM")
    c.connection.commit()

# Timing experiments
def measure_time(func, *args, iterations=100):
    return timeit.timeit(lambda: func(*args), number=iterations) / iterations

def run_experiments(db_name):
    conn, c = setup_database(db_name)
    
    # Prepopulate the database with some data
    if db_name == '1000.sqlite3':
        add_workers_group(c, 1000)
    elif db_name == '10000.sqlite3':
        add_workers_group(c, 10000)
    elif db_name == '100000.sqlite3':
        add_workers_group(c, 100000)

    key_id = 1  # Assume there is a worker with id = 1
    non_key_name = 'some_name'  # Replace with an actual name present in the database
    mask = '%name%'  # Adjust to match actual data

    experiments = {
        "Find by key": (find_by_key, c, key_id),
        "Find by non-key": (find_by_non_key, c, non_key_name),
        "Find by mask": (find_by_mask, c, mask),
        "Add record": (add_worker, c),
        "Add group of records": (add_workers_group, c, 10),
        "Update record by key": (update_worker_by_key, c, key_id),
        "Update record by non-key": (update_worker_by_non_key, c, non_key_name),
        "Delete record by key": (delete_worker_by_key, c, key_id),
        "Delete record by non-key": (delete_worker_by_non_key, c, non_key_name),
        "Delete group of records": (delete_workers_group, c, 10),
        "Vacuum DB after deletion of 200 records": (vacuum_db, c),
    }

    results = {}
    for name, params in experiments.items():
        results[name] = measure_time(*params)
    
    conn.close()
    return results

# Run experiments for each database
databases = ['1000.sqlite3', '10000.sqlite3', '100000.sqlite3']
all_results = {}

for db in databases:
    all_results[db] = run_experiments(db)

# Output results
for db, results in all_results.items():
    print(f"Results for {db}:")
    for name, duration in results.items():
        print(f"{name}: {duration:.6f} seconds")
    print("\n")

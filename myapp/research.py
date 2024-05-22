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

def add_worker(c, name=None):
    c.execute("INSERT INTO WorkersInfo (startwork) VALUES (date('now'))")
    info_id = c.lastrowid
    worker_name = name if name else random_string()
    c.execute("INSERT INTO Workers (name, status, info_id) VALUES (?, ?, ?)", 
              (worker_name, random.choice(['фельдшер', 'медсестра', 'водитель']), info_id))
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
def measure_time(func, *args):
    return timeit.timeit(lambda: func(*args), number=1)

# Compression functions
def compression1(db_name, limit=200):
    start_time = time.time()
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute(f"CREATE TABLE temp_table AS SELECT * FROM Workers EXCEPT SELECT * FROM Workers LIMIT {limit}")
    cursor.execute("DROP TABLE Workers")
    cursor.execute("ALTER TABLE temp_table RENAME TO Workers")
    cursor.execute('VACUUM')
    connection.close()
    end_time = time.time()
    return end_time - start_time

def compression2(db_name):
    start_time = time.time()
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE temp_table AS SELECT * FROM Workers LIMIT 200")
    cursor.execute("DROP TABLE Workers")
    cursor.execute("ALTER TABLE temp_table RENAME TO Workers")
    cursor.execute("VACUUM")
    connection.close()
    end_time = time.time()
    return end_time - start_time

def run_experiments(db_name):
    conn, c = setup_database(db_name)
    
    # Prepopulate the database with some data
    if db_name == '1000.sqlite3':
        num_records = random.randint(1, 1000)
    elif db_name == '10000.sqlite3':
        num_records = random.randint(1, 10000)
    elif db_name == '100000.sqlite3':
        num_records = random.randint(1, 100000)
    
    #add_workers_group(c, num_records)

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
        "Delete group of records": (delete_workers_group, c, 10),
        "Vacuum DB after deletion of 200 records": (compression1, db_name, 200),
        "Vacuum DB after leaving 200 records": (compression2, db_name),
    }

    results = {}
    for name, params in experiments.items():
        if name.startswith("Vacuum DB"):
            results[name] = measure_time(params[0], *params[1:])
        else:
            results[name] = measure_time(*params)
    
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
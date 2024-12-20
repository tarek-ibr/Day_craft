import sqlite3
import hashlib

def searchByUsername(n):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username = ?", (n,))
    row = cursor.fetchone()

    userlist = []
    userlist.append(row[0])
    userlist.append(row[1])

    conn.commit()
    conn.close()

    if row:
        return userlist
    else:
        return None

    # Commit changes and close the connection

def authenticateUser(username, password):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        #print("No user found with this username.")
        conn.close()
        return False
    elif row[1] == hash_password(password):
        conn.commit()
        conn.close()
        return True
    else:
        return False

def checkUserduplicates(username):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return True
    else:
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    if (username == "" or password == ""):
        return False
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return True
    except:
        return False


import sqlite3


def add_task(username, taskname, priority, time, category, prerequisite):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        # Check if the task already exists for the user
        c.execute("SELECT * FROM tasks WHERE username = ? AND taskname = ?", (username, taskname))
        existing_task = c.fetchone()

        if existing_task:
            # Task already exists
            return False

        # Insert the new task
        c.execute("""INSERT INTO tasks (username, taskname, priority, [time], category, prerequisite) VALUES (?, ?, ?, ?, ?, ?) """, (username, taskname, priority, time, category, prerequisite))

        conn.commit()
        return True  # Task added successfully

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def edit_task(username, taskname, priority, time, category, prerequisite):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        # Check if the task exists for the given username and taskname
        c.execute("SELECT * FROM tasks WHERE username = ? AND taskname = ?", (username, taskname))
        existing_task = c.fetchone()

        if not existing_task:
            # Task does not exist
            return False

        # Update the task details using username and taskname as identifiers
        c.execute("""UPDATE tasks SET priority = ?, [time] = ?, category = ?, prerequisite = ? WHERE username = ? AND taskname = ? """, (priority, time, category, prerequisite, username, taskname))

        conn.commit()
        return True  # Task updated successfully

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def get_tasks(username):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        # Correctly pass the username as a single-element tuple
        c.execute("SELECT * FROM tasks WHERE username = ?", (username,))
        tasks = c.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def delete_task(username, taskname):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Execute the DELETE statement
        cursor.execute("DELETE FROM tasks WHERE username = ? AND taskname = ?", (username, taskname))
        conn.commit()

        # Check if any row was deleted
        if cursor.rowcount > 0:
            return True  # Task deleted successfully
        else:
            return False  # No task found with the given criteria
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()



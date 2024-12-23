import sqlite3
import hashlib

def searchByUsername(n):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (n,))
    row = cursor.fetchone()

    userlist = []
    if row:
        userlist.append(row[0])
        userlist.append(row[1])
        userlist.append(row[2])

    conn.commit()
    conn.close()

    return userlist if row else None


def searchByTeamname(n):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams WHERE teamname = ?", (n,))
    row = cursor.fetchone()

    teamlist = []
    if row:
        teamlist.append(row[0])
        teamlist.append(row[1])

    conn.commit()
    conn.close()

    return teamlist if row else None


def authenticateUser(username, password):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row and row[1] == hash_password(password):
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def authenticateTeam(username, password):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams WHERE teamname = ?", (username,))
    row = cursor.fetchone()

    if row and row[1] == hash_password(password):
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def checkUserduplicates(username):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    return row is None


def checkTeamduplicates(username):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams WHERE teamname = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    return row is None


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username, password, team):
    if username == "" or password == "" or team == "":
        return False

    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password, team) VALUES (?, ?, ?)", (username, hashed_password, team))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def add_team(teamname, password):
    if teamname == "" or password == "":
        return False

    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO teams (teamname, password) VALUES (?, ?)", (teamname, hashed_password))
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def add_user_task(username, taskname, priority, time, category, prerequisite, done=0):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM userTasks WHERE username = ? AND taskname = ?", (username, taskname))
        existing_task = c.fetchone()

        if existing_task:
            return False

        c.execute("""INSERT INTO userTasks (username, taskname, priority, time, category, prerequisite, done) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (username, taskname, priority, time, category, prerequisite, done))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def add_team_task(teamname, taskname, priority, time, category, prerequisite, done=0):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM teamTasks WHERE teamname = ? AND taskname = ?", (teamname, taskname))
        existing_task = c.fetchone()

        if existing_task:
            return False

        c.execute("""INSERT INTO teamTasks (teamname, taskname, priority, time, category, prerequisite, done) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                  (teamname, taskname, priority, time, category, prerequisite, done))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def edit_user_task(username, taskname, priority, time, category, prerequisite, done):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM userTasks WHERE username = ? AND taskname = ?", (username, taskname))
        existing_task = c.fetchone()

        if not existing_task:
            return False

        c.execute("""UPDATE userTasks SET priority = ?, [time] = ?, category = ?, prerequisite = ?, done = ? 
                     WHERE username = ? AND taskname = ?""",
                  (priority, time, category, prerequisite, done, username, taskname))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def edit_team_task(teamname, taskname, priority, time, category, prerequisite, done):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM teamTasks WHERE teamname = ? AND taskname = ?", (teamname, taskname))
        existing_task = c.fetchone()

        if not existing_task:
            return False

        c.execute("""UPDATE teamTasks SET priority = ?, time = ?, category = ?, prerequisite = ?, done = ? 
                     WHERE teamname = ? AND taskname = ?""",
                  (priority, time, category, prerequisite, done, teamname, taskname))

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        conn.close()


def get_user_tasks(username):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM userTasks WHERE username = ?", (username,))
        tasks = c.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def get_team_tasks(teamname):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM teamTasks WHERE teamname = ?", (teamname,))
        tasks = c.fetchall()
        return tasks
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def get_team_users(teamname):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()

    try:
        c.execute("SELECT * FROM users WHERE team = ?", (teamname,))
        users = c.fetchall()
        return [user[0] for user in users]
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()


def delete_user_task(username, taskname):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM userTasks WHERE username = ? AND taskname = ?", (username, taskname))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


def delete_team_task(teamname, taskname):
    db_path = "db.sqlite"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM teamTasks WHERE teamname = ? AND taskname = ?", (teamname, taskname))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()

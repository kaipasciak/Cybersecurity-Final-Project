"""
Do a little setup!
Run this setup.py script directly whenever you want a
fresh database to play around with.

"""

import os
import sqlite3
from lessons.password_crack import hash_pw


from db import Db

DIRS = ['instance/var/db',
        'instance/var/log',
        'instance/var/tmp',
        'instance/var/run']

# Create database for final project accounts
def create_db():
    try:
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE accounts (
                userId INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                accessLevel INT
            )''')
        conn.commit()

        # Add first row
        username = 'john_doe'
        password = hash_pw('Password123$')
        accessLevel = 0
        data_to_insert = [(username, password, accessLevel)]
        c.executemany("INSERT INTO accounts (username, password, accessLevel) VALUES (?, ?, ?)", data_to_insert)

        # Add second row
        username = 'jane_smith'
        password = hash_pw('Secret456?')
        accessLevel = 1
        data_to_insert = [(username, password, accessLevel)]
        c.executemany("INSERT INTO accounts (username, password, accessLevel) VALUES (?, ?, ?)", data_to_insert)

        # Add third row
        username = 'admin'
        password = hash_pw('Admin123!')
        accessLevel = 2
        data_to_insert = [(username, password, accessLevel)]
        c.executemany("INSERT INTO accounts (username, password, accessLevel) VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
        print("Files added")
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':

    print("Creating directories...")
    for d in DIRS:
        try:
            os.makedirs(d)
        except FileExistsError:
            pass

    print("Initializing database...")
    Db.setup()

    print("Done!")

    create_db()

    permissions = {}
    try:
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM accounts"):
            permissions[row[1]] = [row[0], row[2], row[3]]
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

    print(permissions)




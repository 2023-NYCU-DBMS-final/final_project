import sqlite3
import base64
import hashlib

def checklogin(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashlib.sha256(password.encode()).hexdigest()))
    result = c.fetchall()
    conn.close()
    return bool(result)

def add_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    """
        check if username already exists
    """


    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    # Check if the user was successfully added
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    result = c.fetchall()
    conn.close()
    return bool(result)

def checkcookie(cookie):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (base64.b64decode(cookie).decode(),))
    result = c.fetchall()
    conn.close()
    return bool(result)
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def showlogin():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def showsignup():
    return render_template('signup.html')

@app.route('/showdata', methods=['GET'])
def showdata():
    return render_template('data.html')

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

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    username.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")
    password.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")

    if checklogin(username, password):
        # Set a cookie upon successful login
        response = make_response('Login successful')
        response.set_cookie('user', username)
        return response
    else:
        return 'Login failed'

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    username.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")
    password.replace('"',"").replace("'","").replace(";","")\
    .replace(" ","").replace("=","").replace("(","").replace(")","")\
    .replace("\\","").replace("/","")

    # Add your signup logic here
    # For simplicity, I'm assuming that the username is unique
    # In a real application, you'd need to check for existing usernames, handle password hashing, etc.
    if(add_user(username, password)):
        return 'Signup successful'
    else:
        return 'Signup failed'

@app.route('/userpage')
def userpage():
    # Check if the user is logged in (you need to implement this logic)
    username = request.cookies.get('user')

    if username:
        return render_template('userpage.html', username=username)
    else:
        # Redirect to login page with an alert
        response = make_response(redirect(url_for('loginpage')))
        response.set_cookie('alert', 'Please login first')
        return response

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Add your authentication logic here
    # For example, you can use a database to check the credentials
    # For simplicity, I'm using a hardcoded username and password
    if username == 'admin' and password == 'password':
        return 'Login successful'
    else:
        return 'Login failed'

if __name__ == '__main__':
    app.run(debug=True)

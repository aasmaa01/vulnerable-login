from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Set up the database with more realistic test users
DB_NAME = 'combat_users.db'

def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)  # Reset DB every run for demo purposes

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )''')
    c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    c.execute("INSERT INTO users (username, password, role) VALUES ('lyna', 'letmein', 'user')")
    c.execute("INSERT INTO users (username, password, role) VALUES ('assia', 'azerty', 'user')")
    conn.commit()
    conn.close()

LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cyber Combat Login</title>
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: #fff;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            width: 320px;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        input[type="submit"] {
            background-color: #2980b9;
            color: white;
            border: none;
            padding: 10px;
            width: 100%;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        input[type="submit"]:hover {
            background-color: #1c5980;
        }
        .message {
            margin-top: 15px;
            font-weight: bold;
            color: #e74c3c;
        }
        .message.success {
            color: #27ae60;
        }
        footer {
            margin-top: 20px;
            font-size: 12px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>Red Team Demo</h1>
        <form method="POST">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <input type="submit" value="Login">
        </form>
        {% if message %}
            <p class="message {% if 'successful' in message %}success{% endif %}">{{ message }}</p>
        {% endif %}
        <footer>
            Created by Asma | <a href="https://github.com/aasmaa01" style="color:#2980b9;">@aasmaa01</a>
        </footer>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # STILL VULNERABLE: raw string interpolation (SQLi possible)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[DEBUG] Executing SQL: {query}")
        try:
            c.execute(query)
            result = c.fetchone()
        except sqlite3.Error as e:
            message = f"SQL error: {e}"
            result = None

        conn.close()

        if result:
            message = f"Login successful! Welcome, {result[1]} ({result[3]})"
        elif "'" in username or "'" in password:
            message = "Suspicious input detected."
        else:
            message = "Login failed. Try again."

    return render_template_string(LOGIN_PAGE, message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import subprocess

app = Flask(__name__, static_folder='static')

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'game_db'

mysql = MySQL(app)

# Route for the login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for('home'))  # Redirect to home after login
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user (username,password,email) VALUES ( %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

# Route for the home page (game level selection)
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('index_1.html')
    return redirect(url_for('login'))  # Redirect to login if not logged in

# Route to handle level selection
@app.route('/start_game', methods=['POST'])
def start_game():
    selected_level = request.form.get('level')  # Get the selected level from the form
    # Start the game in a separate process using subprocess
    subprocess.Popen(['python', 'main.py', selected_level])
    return redirect(url_for('game'))


# Route to update the player's score
@app.route('/update_score', methods=['POST'])
def update_score():
    if 'loggedin' in session:  # Make sure the user is logged in
        score_data = request.get_json()  # Get the score from the request
        username = session['username']  # Retrieve the username from the session
        new_score = score_data['score']  # Get the new score from the JSON data

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Update the score in the database if the new score is higher than the previous one
        cursor.execute('SELECT score FROM accounts WHERE username = %s', (username,))
        result = cursor.fetchone()
        if result and result['score'] < new_score:  # Only update if the new score is higher
            cursor.execute('UPDATE accounts SET score = %s WHERE username = %s', (new_score, username))
            mysql.connection.commit()
            return 'Score updated successfully!'
        return 'No update needed.'
    return 'User not logged in.', 401


# Route for the game page
@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)

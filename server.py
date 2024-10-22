from flask import Flask, render_template, request, jsonify, make_response,redirect, url_for, session
from train import chat
from flask_bcrypt import Bcrypt
import mysql.connector
app = Flask(__name__)
app.secret_key = 'your_secret_key'

bcrypt = Bcrypt(app)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='admin'
    )
    return connection
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = 'Username already exists. Please choose another one.'
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
            connection.commit()
            message = 'You have successfully registered!'

        cursor.close()
        connection.close()
        return render_template('data/register.html', message=message)
    
    return render_template('data/register.html', message=message)

@app.route('/a', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and bcrypt.check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return render_template('index.html')
        else:
            message = 'Login unsuccessful. Please check your username and password.'
    
    return render_template('data/login.html', message=message)

@app.route("/login")
def enty():
	return render_template('data/login.html')

@app.route("/about")
def ent():
	return render_template('about.html')



@app.route("/contact")
def etxc():
	return render_template('contatct.html')

@app.route('/', methods = ['GET', 'POST'])
def indexpage():
	if request.method == "POST":

		print(request.form.get('name'))
		return render_template("index.html")
	return render_template("index.html")

@app.route("/entry", methods=['POST'])
def entry():
	req = request.get_json()
	print(req)
	res = make_response(jsonify({"name":"{}.".format(chat(req)),"message":"OK"}), 200)
	return res
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(debug=True)

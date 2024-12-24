from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "12345678" 

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shreyash1@#',
    'database': 'users'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        if name and email and role:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, role) VALUES (%s, %s, %s)", (name, email, role))
            conn.commit()
            conn.close()
            flash("User added successfully!")
            return redirect(url_for('users'))
        else:
            flash("All fields are required!")
    
    return render_template('new_user.html')

@app.route('/users/<int:id>')
def user_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return "User not found!", 404
    return render_template('user_details.html', user=user)

@app.errorhandler(404)
def not_found_error(e):
    return "Resource not found!", 404

if __name__ == "__main__":
    app.run(debug=True)

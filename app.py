from flask import Flask, request, jsonify, render_template, redirect, session
from werkzeug.security import generate_password_hash

import bcrypt
import os

from functools import wraps

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

from database import db

from database import (
    insert_health_data,
    get_all_health_data,
    delete_health_record,
    update_health_data,
    get_health_record,
    create_user,
    get_user_by_username,
    get_user_by_id
)



def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper



# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user['password_hash'].encode('utf-8')
        ):

            session['user_id'] = user['id']

            return redirect('/dashboard')

        return "Invalid username or password"

    return render_template('login.html')

# Register 
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        create_user(username, password)

        return redirect('/login')

    return render_template('register.html')

#logout
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

#profile
@app.route("/profile")
@login_required
def profile():

    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    user = get_user_by_id(user_id)

    if not user:
        return "User not found"

    return render_template("profile.html", user=user)

#change password
@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():

    user_id = session.get("user_id")

    if request.method == "POST":

        new_password = request.form["password"]

        password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE id = %s
            """,
            (password_hash, user_id)
        )

        db.commit()
        cursor.close()

        return redirect("/profile")

    return render_template("change_password.html")

#Routes 

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/add-health', methods=['GET', 'POST'])
@login_required
def add_health():

    if request.method == 'POST':

        systolic = request.form['systolic']
        diastolic = request.form['diastolic']
        blood_sugar = request.form['blood_sugar']
        weight = request.form['weight']
        height = request.form['height']

        insert_health_data(
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height,
        session['user_id']
)
        return redirect('/dashboard')

    return render_template('add_health.html')

@app.route('/dashboard')
@login_required
def dashboard():

    data = get_all_health_data(session['user_id'])

    # Calculate BMI dynamically
    for row in data:
        weight = row.get('weight_lb')
        height = row.get('height_in')

        if weight and height:
            height_m = float(height) * 0.0254
            bmi = float(weight) * 0.453592 / (height_m ** 2)
            row['bmi'] = round(bmi, 2)
        else:
            row['bmi'] = None

    return render_template("dashboard.html", data=data)


@app.route('/history')
def history():
    return render_template('history.html')


# Insert data
@app.route('/add', methods=['POST'])
def add_data():

    data = request.json

    insert_health_data(
        data['systolic'],
        data['diastolic'],
        data['blood_sugar'],
        data['weight'],
        data['height'],
        data['bmi']
    )

    return jsonify({"message": "Data inserted successfully"})


# Get data
@app.route('/data')
@login_required
def get_data():

    data = get_all_health_data(session['user_id'], order="ASC")

    # Compute BMI dynamically
    for row in data:
        weight = row.get('weight_lb')
        height = row.get('height_in')

        if weight and height:
            height_m = float(height) * 0.0254
            bmi = float(weight) * 0.453592 / (height_m ** 2)
            row['bmi'] = round(bmi, 2)
        else:
            row['bmi'] = None

    return jsonify(data)

# delete
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):

	delete_health_record(id)

	return redirect('/dashboard')

# edit (GET)
@app.route('/edit/<int:id>')
def edit(id):

    record = get_health_record(id)    

    return render_template('edit.html', record=record)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    systolic = request.form['systolic']
    diastolic = request.form['diastolic']
    blood_sugar = request.form['blood_sugar']
    weight = request.form['weight']
    height = request.form['height']

    update_health_data(
    	id,
	systolic,
	diastolic,
	blood_sugar,
	weight,
	height,
	session["user_id"]
)
    return redirect('/dashboard')

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

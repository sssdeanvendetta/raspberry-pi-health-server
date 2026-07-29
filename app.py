from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="health_user",
    password=os.getenv("DB_PASSWORD"),
    database="health_manager"
)


def insert_health_data(systolic, diastolic, blood_sugar, weight, height, bmi):

    cursor = db.cursor()

    query = """
    INSERT INTO health_metrics 
    (systolic, diastolic, blood_sugar_mg_dl, weight_lb, height_in, bmi)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height,
        bmi
    )

    cursor.execute(query, values)
    db.commit()

    cursor.close()

#Routes 

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/add-health', methods=['GET', 'POST'])
def add_health():

    if request.method == 'POST':

        systolic = request.form['systolic']
        diastolic = request.form['diastolic']
        blood_sugar = request.form['blood_sugar']
        weight = request.form['weight']
        height = request.form['height']

        # Calculate BMI
        height_m = float(height) * 0.0254
        bmi = round(float(weight) * 0.453592 / (height_m ** 2), 2)

        insert_health_data(
            systolic,
            diastolic,
            blood_sugar,
            weight,
            height,
            bmi
        )

        return redirect('/dashboard')

    return render_template('add_health.html')
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

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
def get_data():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM health_metrics
        ORDER BY date_time ASC
    """)

    data = cursor.fetchall()

    cursor.close()

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

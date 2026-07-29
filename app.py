from flask import Flask, request, jsonify, render_template
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

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/add-health')
def add_health():
    return render_template("add_health.html")


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
    cursor = db.cursor()

    query = """
    INSERT INTO health_metrics 
    (systolic, diastolic, blood_sugar_mg_dl, weight_lb, height_in, bmi)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        data['systolic'],
        data['diastolic'],
        data['blood_sugar'],
        data['weight'],
        data['height'],
        data['bmi']
    )

    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Data inserted successfully"})

# Get data
@app.route('/data', methods=['GET'])
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM health_metrics ORDER BY date_time DESC")
    result = cursor.fetchall()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

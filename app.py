from flask import Flask, request, jsonify, render_template, redirect
from database import db

app = Flask(__name__)


def insert_health_data(systolic, diastolic, blood_sugar, weight, height):

    cursor = db.cursor()

    query = """
    INSERT INTO health_metrics 
    (systolic, diastolic, blood_sugar_mg_dl, weight_lb, height_in)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height
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
            height
        )

        return redirect('/dashboard')

    return render_template('add_health.html')

@app.route('/dashboard')
def dashboard():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM health_metrics
        ORDER BY date_time DESC
    """)

    data = cursor.fetchall()
    cursor.close()

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
def get_data():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM health_metrics
        ORDER BY date_time ASC
    """)

    data = cursor.fetchall()

    cursor.close()

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

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM health_metrics WHERE id = %s",
        (id,)
    )

    db.commit()
    cursor.close()

    return redirect('/dashboard')

# edit (GET)
@app.route('/edit/<int:id>')
def edit(id):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM health_metrics WHERE id = %s",
        (id,)
    )

    record = cursor.fetchone()
    cursor.close()
    print(record)

    return render_template('edit.html', record=record)

# Update (POST) 
@app.route('/update/<int:id>', methods=['POST'])
def update(id):

    systolic = request.form['systolic']
    diastolic = request.form['diastolic']
    blood_sugar = request.form['blood_sugar']
    weight = request.form['weight']
    height = request.form['height']
 
    height_m = float(height) * 0.0254
    bmi = round(float(weight) * 0.453592 / (height_m ** 2), 2)

    cursor = db.cursor()

    cursor.execute("""
     UPDATE health_metrics
      SET systolic=%s,
         diastolic=%s,
         blood_sugar_mg_dl=%s,
         weight_lb=%s,
         height_in=%s
     WHERE id=%s""", (systolic, diastolic, blood_sugar, weight, height,id))
    db.commit()
    cursor.close()

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

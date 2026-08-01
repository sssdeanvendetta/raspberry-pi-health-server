from flask import Flask, request, jsonify, render_template, redirect

from database import (
    insert_health_data,
    get_all_health_data,
    delete_health_record,
    update_health_data,
    get_health_record
)

app = Flask(__name__)



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

    data = get_all_health_data()

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

    data = get_all_health_data(order="ASC")

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
        height
    )

    return redirect('/dashboard')

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

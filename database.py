import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
    host="127.0.0.1",
    user="health_user",
    password=os.getenv("DB_PASSWORD"),
    database="health_manager"
)


# Insert health data
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



# Get all health records
def get_all_health_data(order="DESC"):

    cursor = db.cursor(dictionary=True)

    query = f"""
        SELECT *
        FROM health_metrics
        ORDER BY date_time {order}
    """

    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()

    return data

#get single record

def get_health_record(id):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM health_metrics WHERE id = %s",
        (id,)
    )

    record = cursor.fetchone()

    cursor.close()

    return record




# Delete health record
def delete_health_record(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM health_metrics WHERE id = %s",
        (id,)
    )

    db.commit()

    cursor.close()



# Update health record
def update_health_data(id, systolic, diastolic, blood_sugar, weight, height):

    cursor = db.cursor()

    cursor.execute("""
        UPDATE health_metrics
        SET systolic=%s,
            diastolic=%s,
            blood_sugar_mg_dl=%s,
            weight_lb=%s,
            height_in=%s
        WHERE id=%s
    """,
    (
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height,
        id
    ))

    db.commit()

    cursor.close()
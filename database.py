import mysql.connector
import os
import bcrypt
from dotenv import load_dotenv
import time

load_dotenv()

for i in range(10):
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        break
    except:
        print("Waiting for DB...")
        time.sleep(3)


# get user

def get_user_by_id(user_id):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (user_id,)
    )

    user = cursor.fetchone()
    cursor.close()

    return user

# Create user
def create_user(username, password):

    cursor = db.cursor()

    password_hash = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
).decode('utf-8')

    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, password_hash)
    )

    db.commit()
    cursor.close()


# Get user by username
def get_user_by_username(username):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )

    user = cursor.fetchone()
    cursor.close()

    return user

# Insert health data
def insert_health_data(systolic, diastolic, blood_sugar, weight, height, user_id):

   
    cursor = db.cursor()

    query = """
    INSERT INTO health_metrics 
    (systolic, diastolic, blood_sugar_mg_dl, weight_lb, height_in, user_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height,
        user_id
    )

    cursor.execute(query, values)
    db.commit()

    cursor.close()
   


# Get all health records
def get_all_health_data(user_id, order="DESC"):

    cursor = db.cursor(dictionary=True)

    if order not in ["ASC", "DESC"]:
        order = "DESC"

    query = f"""
        SELECT *
        FROM health_metrics
        WHERE user_id = %s
        ORDER BY date_time {order}
    """

    cursor.execute(query, (user_id,))

    data = cursor.fetchall()

    cursor.close()

    return data
#get single record

def get_health_record(id, user_id):

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM health_metrics
        WHERE id=%s AND user_id=%s
        """,
        (id, user_id)
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
def update_health_data(id, systolic, diastolic, blood_sugar, weight, height, user_id):

    cursor = db.cursor()

    cursor.execute("""
        UPDATE health_metrics
        SET systolic=%s,
            diastolic=%s,
            blood_sugar_mg_dl=%s,
            weight_lb=%s,
            height_in=%s
        WHERE id=%s AND user_id=%s
    """,
    (
        systolic,
        diastolic,
        blood_sugar,
        weight,
        height,
        id,
        user_id
    ))

    db.commit()

    cursor.close()
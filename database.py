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

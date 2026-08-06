CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE health_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    systolic INT,
    diastolic INT,
    blood_sugar_mg_dl FLOAT,
    weight_lb FLOAT,
    height_in FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
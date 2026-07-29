# Raspberry Pi Health Monitoring Server

## 🚀 Overview

A full-stack health monitoring system running on a Raspberry Pi 4.
It captures health metrics (blood sugar, blood pressure, weight), stores them in MariaDB, and visualizes trends through a dynamic web dashboard.

---

## ⚡ One Command Startup

```bash
chmod +x run.sh
./run.sh
```

---

## 📊 Key Features

* Interactive dashboard (Chart.js)
* Dynamic metric switching (Sugar, BP, Weight)
* Date filtering (7 days, 30 days, all)
* Real-time summaries (avg, max, min)
* REST API for data access
* Secure environment-based configuration

---

## 🏗️ Architecture

```
Browser UI
   ↓
Flask API
   ↓
MariaDB
   ↓
Raspberry Pi (Linux)
```

---

## ⚙️ Tech Stack

* Flask (Python)
* MariaDB
* Chart.js
* HTML/CSS/JavaScript
* Raspberry Pi OS (Linux)

---

## 📁 Structure

```
app.py
run.sh
templates/
static/
screenshots/
```

---

## 🔌 API

**GET /data** → Retrieve health records
**POST /add** → Insert health data

```json
{
  "systolic": 120,
  "diastolic": 80,
  "blood_sugar": 140,
  "weight": 218,
  "height": 68,
  "bmi": 33
}
```

---

## 🧠 What This Shows

* End-to-end system design (frontend → backend → database)
* API development & data handling
* Linux server deployment
* Secure configuration practices
* Real-world debugging and iteration

---

## 💼 Why It Matters

This project demonstrates practical, job-ready skills in backend development, system integration, and data visualization—built and deployed on real hardware.

---

## 📸 Screenshots

![API Response](screenshots/api-response.png)
![Flask Server](screenshots/flask-server-running.png)
![Raspberry Pi Setup](screenshots/raspberry-pi-setup.jpeg)

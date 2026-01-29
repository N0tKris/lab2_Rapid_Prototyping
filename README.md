# Rapid Prototyping Catalog Management System

## Overview
This project is a rapid prototype of a catalog management system. It demonstrates a modular architecture with a Python Flask frontend, a Java Spring Boot backend, and a CSV file as the database. Users can view, add, and edit catalog items through a web interface. A simple login system is included.

---

## Requirements

### Backend (Java)
- Java 17+ (or compatible with Spring Boot 3.x)
- Maven (wrapper included: `./mvnw`)

### Frontend (Python)
- Python 3.8+
- pip
- Flask
- requests

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd lab2_Rapid_Prototyping
```

### 2. Prepare the Backend
```bash
cd backend
# On Linux/macOS:
./mvnw spring-boot:run
# On Windows:
./mvnw.cmd spring-boot:run
```
The backend will start on [http://localhost:8080](http://localhost:8080)

### 3. Prepare the Frontend
```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
The frontend will start on [http://localhost:5000](http://localhost:5000)

---

## Usage
1. Open [http://localhost:5000](http://localhost:5000) in your browser.
2. Login with:
   - **Username:** admin
   - **Password:** password
3. View, add, or edit catalog items. All changes are saved to `catalog.csv`.

---

## File Structure
- `backend/` - Java Spring Boot backend (REST API)
- `frontend/` - Python Flask frontend (web UI)
- `catalog.csv` - CSV file database for catalog items

---

## Notes
- The backend and frontend must both be running for full functionality.
- The backend reads and writes to `catalog.csv` in the project root.
- The login system is for demonstration only (credentials are hardcoded).

---

## Extending the Prototype
- Add more fields to `catalog.csv` and update the model/UI accordingly.
- Replace the CSV with a real database for production use.
- Improve validation and error handling.
- Add user management and authentication features.

---

## License
This project is for educational purposes.

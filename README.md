# Catalog Management System

## Overview

This repository contains a catalog management system used throughout
**CSCI 2040U – Software Design and Analysis** for **multiple labs and exercises**.

The project began as a rapid prototype in **Lab 2**, and is extended, refactored,
and reused in subsequent labs to demonstrate core software design concepts,
including separation of concerns, modularity, client–server interaction, and
incremental development.

The system consists of:

* a Java Spring Boot backend exposing a REST API
* a Python frontend (CLI and GUI options)
* a CSV file used as persistent storage

---

## Project Structure

```
.
├── backend/        # Java Spring Boot backend (REST API)
├── frontend/       # Python frontend (CLI + Tkinter GUI)
├── catalog.csv     # Persistent datastore (CSV)
└── README.md
```

---

## Tech Stack

### Backend

* Java 17+
* Spring Boot (3.x)
* Maven (wrapper included)

### Frontend

* Python 3.8+
* requests
* Tkinter (for GUI)

### Data Storage

* CSV file (catalog.csv)

---

## Purpose (Course Context)

This repository is used across **multiple labs**, including but not limited to:

* Rapid prototyping
* API design
* Frontend–backend integration
* Refactoring and design improvement
* Testing and maintainability exercises

Each lab may build on, modify, or extend the existing codebase.

---

## API

**Base URL:**

```
http://localhost:8080/api/catalog
```

The backend handles:

* CSV reads/writes
* Basic validation
* CRUD operations on catalog items

---

## Prerequisites

* **Java 17 (JDK 17)** installed and available on PATH
* No separate Maven install required (Maven wrapper included)
* **Python 3.8+**
* On Linux: `python3-tk` may be required for the GUI
* VS Code or IntelliJ recommended

---

## Run Locally (Recommended)

### 1) Start the backend

From the repository root:

```bash
cd backend
./mvnw spring-boot:run
```

Verify it’s running:

```bash
curl http://localhost:8080/api/catalog
```

Expected: HTTP 200 and a JSON array (possibly empty).

---

### 2) Set up Python frontend

From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate
pip install -r frontend/requirements.txt
```

---

### 3) Run a frontend

**CLI:**

```bash
python3 frontend/cli_app.py
```

**GUI:**

```bash
python3 frontend/gui3.py
```

If the GUI fails on Linux:

```bash
sudo apt-get install python3-tk
```

---

## Data Handling

* The backend looks for `catalog.csv` in the following order:

  1. current working directory
  2. parent directory
  3. `backend/catalog.csv`

If no file is found, a new `catalog.csv` is created automatically with headers.

**Important:**
For predictable behavior, start the backend from the `backend/` directory.

---

## Troubleshooting

* **Cannot connect to backend**

  * Ensure Spring Boot is running
  * Ensure port `8080` is free
* **Python dependency errors**

  * Activate the virtual environment
  * Re-run `pip install -r frontend/requirements.txt`
* **Java errors**

  * Confirm `java -version` reports Java 17

---

## Development Notes

* Java dependencies are managed via Maven (`backend/pom.xml`)
* Python dependencies are listed in `frontend/requirements.txt`
* Do **not** add a `requirements.txt` for Java
* Update Python deps with:

  ```bash
  pip freeze > frontend/requirements.txt
  ```

---

## Optional Improvements

This repo can be extended with:

* a script to start backend + frontend together
* a `Makefile` for common commands
* cleanup of unused Python dependencies
* additional tests and validation layers

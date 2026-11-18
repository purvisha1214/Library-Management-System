# Library Management System

A Python and MySQL-based Library Management System that helps manage books, members, and book transactions through a simple menu-driven interface.

## Features

- Add new books
- View all available books
- Register library members
- Issue books to members
- Return issued books
- View complete transaction history
- Automatically update available book copies
- Store records in a MySQL database

## Technologies Used

- Python
- MySQL
- MySQL Connector/Python

## Project Structure

```text
LibraryManagementSystem/
│
├── main.py
├── database.py
├── config.py
├── schema.sql
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd LibraryManagementSystem
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create the database

Open MySQL Workbench and execute the SQL commands from `schema.sql`.

### 4. Configure database connection

Create a local `config.py` file and add your own MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "library_db"
}
```

Do not upload your actual database password to GitHub.

### 5. Run the project

```bash
python main.py
```

## Author

Developed as a Python and MySQL academic project.
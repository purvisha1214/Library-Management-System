
# 📚 Library Management System

A Python-based Library Management System built using Streamlit and MySQL. This application helps manage books, members, book issuing, returns, and transaction records through a user-friendly web interface.

## 🚀 Features

- Dashboard with library statistics
- Add and view books
- Search books by title or author
- Register and view members
- Issue books to registered members
- Return issued books
- View transaction history
- Filter transactions by status
- Low-stock book alerts
- Recent transaction overview
- Export books, members, and transactions as CSV files

## 🛠️ Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- MySQL Connector

## 📁 Project Structure

```text
LibraryManagementSystem/
│
├── app.py
├── main.py
├── database.py
├── config.py
├── schema.sql
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/purvisha1214/Library-Management-System.git
```

### 2. Open the project folder

```bash
cd Library-Management-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up MySQL

- Open MySQL Workbench.
- Run the SQL commands in `schema.sql`.
- Create a local `config.py` file with your own MySQL database credentials.
- Do not upload your database password to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

- Database credentials are stored locally in `config.py`.
- Sensitive configuration files are excluded using `.gitignore`.
- Database operations use parameterized SQL queries.

## 👩‍💻 Author

**Purvisha Gohel**

BCA Student | Aspiring Software Developer

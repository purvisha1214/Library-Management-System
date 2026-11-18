
# 📚 Library Management System

A Python-based Library Management System built using Streamlit and MySQL. It helps manage books, members, book issuing, returns, and transaction records through a web interface.

## 🚀 Features

- Dashboard with library statistics
- Add and view books
- Search books by title or author
- Register and view members
- Issue books to members
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
- MySQL Connector/Python

## 📁 Project Structure

```text
LibraryManagementSystem/
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
cd Library-Management-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up MySQL

- Open MySQL Workbench.
- Execute the SQL commands in `schema.sql`.
- Create a local `config.py` file with your own MySQL credentials.
- Do not upload your actual database password to GitHub.

### 4. Run the application

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

import mysql.connector
import streamlit as st

try:
    from config import DB_CONFIG
    DB_CONFIG = DB_CONFIG.copy()

except ImportError:
    DB_CONFIG = dict(st.secrets["mysql"])


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

        connection.close()
        return None

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None
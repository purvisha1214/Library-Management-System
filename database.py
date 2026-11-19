import streamlit as st
import mysql.connector

try:
    from config import DB_CONFIG
except ImportError:
    DB_CONFIG = dict(st.secrets["mysql"])


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            print("Database Connected Successfully!")
            return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)

    return None
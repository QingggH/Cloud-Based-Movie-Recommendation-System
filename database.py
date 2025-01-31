import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration, retrieved from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  
    'database': os.getenv('DB_NAME', 'recommend')
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def initialize_database():
    """初始化数据库和表"""

    # Connect to MySQL default database
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')  
    )
    cursor = connection.cursor()

    # Create 'recommend' database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'recommend')}")
    connection.commit()
    connection.close()

    # Now connect to 'recommend' database and create tables
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movieId INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genres VARCHAR(255)
        )
    """)
    connection.commit()
    connection.close()

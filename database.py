import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),  
    'database': os.getenv('DB_NAME', 'recommend')
}

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ 成功连接到数据库:", DB_CONFIG["database"])
        return conn
    except mysql.connector.Error as err:
        print("❌ 数据库连接失败:", err)
        exit(1)

def table_exists(cursor, table_name):
    """检查表是否存在"""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def initialize_database():
    try:
        print("🔹 连接 MySQL 服务器...")
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        cursor = connection.cursor()

        print("🔹 创建数据库（如果不存在）...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'recommend')}")
        connection.commit()
        connection.close()

        print("🔹 连接到 recommend 数据库...")
        connection = get_connection()
        cursor = connection.cursor()

        print("🔹 检查并创建 tables ...")

        tables = {
            "users": """
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """,
            "movies": """
                CREATE TABLE movies (
                    movieId INT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL
                )
            """,
            "genres": """
                CREATE TABLE genres (
                    genreId INT AUTO_INCREMENT PRIMARY KEY,
                    genre VARCHAR(255) UNIQUE NOT NULL
                )
            """,
            "movies_genres": """
                CREATE TABLE movies_genres (
                    movieId INT NOT NULL,
                    genreId INT NOT NULL,
                    PRIMARY KEY (movieId, genreId),
                    FOREIGN KEY (movieId) REFERENCES movies(movieId),
                    FOREIGN KEY (genreId) REFERENCES genres(genreId)
                )
            """,
            "ratings": """
                CREATE TABLE ratings (
                    userId INT NOT NULL,
                    movieId INT NOT NULL,
                    rating DECIMAL(2,1) NOT NULL,
                    timestamp INT NOT NULL,
                    PRIMARY KEY (userId, movieId)
                )
            """,
            "links": """
                CREATE TABLE links (
                    movieId INT PRIMARY KEY,
                    imdbId VARCHAR(30),
                    tmdbId VARCHAR(30)
                )
            """,
            "tags": """
                CREATE TABLE tags (
                    userId INT NOT NULL,
                    movieId INT NOT NULL,
                    tag VARCHAR(255) NOT NULL,
                    timestamp INT NOT NULL,
                    PRIMARY KEY (userId, movieId, tag)
                )
            """
        }

        for table_name, create_query in tables.items():
            if not table_exists(cursor, table_name):
                cursor.execute(create_query)
                print(f"✅ Created `{table_name}` table")
            else:
                print(f"🔹 `{table_name}` 表已存在，跳过创建")

        connection.commit()
        connection.close()
        print("🎉 数据库初始化完成！")

    except mysql.connector.Error as err:
        print("❌ MySQL 错误:", err)
    except Exception as e:
        print("❌ 发生异常:", e)

if __name__ == "__main__":
    initialize_database()
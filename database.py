import mysql.connector
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 数据库配置，从环境变量中获取
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

    # 连接 MySQL 默认数据库（避免尝试连接 recommend 而报错）
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')  
    )
    cursor = connection.cursor()

    # 创建 recommend 数据库
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME', 'recommend')}")
    connection.commit()
    connection.close()

    # 现在连接 recommend 数据库，并创建表
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

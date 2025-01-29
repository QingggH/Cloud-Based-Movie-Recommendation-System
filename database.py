import mysql.connector

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'hyq200066',  
    'database': 'recommend'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def initialize_database():
    """初始化数据库和表"""

    # 连接 MySQL 默认数据库（避免尝试连接 recommend 而报错）
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="hyq200066"  
    )
    cursor = connection.cursor()

    # 创建 recommend 数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS recommend")
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

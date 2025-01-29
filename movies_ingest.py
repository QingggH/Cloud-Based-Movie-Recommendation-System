import csv
from database import get_connection

def ingest_movies(csv_file):
    """将 movies.csv 数据导入数据库"""
    connection = get_connection()
    cursor = connection.cursor()

    # 清空旧表数据
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
        CREATE TABLE movies (
            movieId INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genres VARCHAR(255)
        )
    """)

    # 插入新数据
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO movies (movieId, title, genres) VALUES (%s, %s, %s)
            """, (int(row['movieId']), row['title'], row['genres']))

    connection.commit()
    connection.close()
    print("数据导入成功！")

if __name__ == '__main__':
    ingest_movies('ml-latest-small/movies.csv')
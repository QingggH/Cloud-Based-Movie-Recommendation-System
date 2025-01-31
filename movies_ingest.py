import csv
from database import get_connection

def ingest_movies(csv_file):
    """Import movies.csv data into the database"""
    connection = get_connection()
    cursor = connection.cursor()

    # Clear old table data
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
        CREATE TABLE movies (
            movieId INT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genres VARCHAR(255)
        )
    """)

    # Insert new data
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT INTO movies (movieId, title, genres) VALUES (%s, %s, %s)
            """, (int(row['movieId']), row['title'], row['genres']))

    connection.commit()
    connection.close()
    print("Data import successful!")

if __name__ == '__main__':
    ingest_movies('ml-latest-small/movies.csv')
import csv
from database import get_connection

def ingest_movies(csv_file):
    connection = get_connection()
    cursor = connection.cursor()

    print("🔹 开始清空旧数据...")
    cursor.execute("DELETE FROM movies")
    cursor.execute("DELETE FROM genres")
    cursor.execute("DELETE FROM movies_genres")
    connection.commit()

    genre_map = {}

    print(f"🔹 读取 {csv_file} 并开始插入数据...")
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0  

        for row in reader:
            movie_id = int(row['movieId'])
            title = row['title']
            genres = row['genres'].split('|')

            cursor.execute("INSERT INTO movies (movieId, title) VALUES (%s, %s)", (movie_id, title))
            count += 1

            for genre in genres:
                if genre not in genre_map:
                    cursor.execute("INSERT IGNORE INTO genres (genre) VALUES (%s)", (genre,))
                    connection.commit()  
                    
                    cursor.execute("SELECT genreId FROM genres WHERE genre = %s", (genre,))
                    genre_id = cursor.fetchone()
                    
                    if genre_id:
                        genre_map[genre] = genre_id[0]
                    else:
                        print(f"⚠️ 警告：未找到 genreId for {genre}")

                if genre in genre_map:
                    cursor.execute("INSERT INTO movies_genres (movieId, genreId) VALUES (%s, %s)", (movie_id, genre_map[genre]))
#
    connection.commit()
    connection.close()
    print(f"✅ {count} 部电影导入成功！")

def ingest_ratings(csv_file):
    connection = get_connection()
    cursor = connection.cursor()

    print("🔹 开始清空 ratings 表...")
    cursor.execute("DELETE FROM ratings")
    connection.commit()

    print(f"🔹 读取 {csv_file} 并开始插入数据...")
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0

        for row in reader:
            cursor.execute("INSERT INTO ratings (userId, movieId, rating, timestamp) VALUES (%s, %s, %s, %s)", 
                           (row['userId'], row['movieId'], row['rating'], row['timestamp']))
            count += 1

    connection.commit()
    connection.close()
    print(f"✅ {count} 条评分记录导入成功！")

def ingest_links(csv_file):
    connection = get_connection()
    cursor = connection.cursor()

    print("🔹 开始清空 links 表...")
    cursor.execute("DELETE FROM links")
    connection.commit()

    print(f"🔹 读取 {csv_file} 并开始插入数据...")
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0

        for row in reader:
            cursor.execute("INSERT INTO links (movieId, imdbId, tmdbId) VALUES (%s, %s, %s)", 
                           (row['movieId'], row['imdbId'], row['tmdbId']))
            count += 1

    connection.commit()
    connection.close()
    print(f"✅ {count} 条电影链接数据导入成功！")

def ingest_tags(csv_file):
    connection = get_connection()
    cursor = connection.cursor()

    print("🔹 开始清空 tags 表...")
    cursor.execute("DELETE FROM tags")
    connection.commit()

    print(f"🔹 读取 {csv_file} 并开始插入数据...")
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0

        for row in reader:
            cursor.execute("INSERT INTO tags (userId, movieId, tag, timestamp) VALUES (%s, %s, %s, %s)", 
                           (row['userId'], row['movieId'], row['tag'], row['timestamp']))
            count += 1

    connection.commit()
    connection.close()
    print(f"✅ {count} 条标签数据导入成功！")

    

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("❌ 用法: python movies_ingest.py <数据类型> <CSV路径>")
        print("例如: python movies_ingest.py movies dataset/movies.csv")
        exit(1)

    data_type = sys.argv[1]
    csv_file = sys.argv[2]

    if data_type == "movies":
        ingest_movies(csv_file)
    elif data_type == "ratings":
        ingest_ratings(csv_file)
    elif data_type == "links":
        ingest_links(csv_file)
    elif data_type == "tags":
        ingest_tags(csv_file)
    else:
        print("❌ 无效的数据类型！请选择 movies / ratings / links/ tags")
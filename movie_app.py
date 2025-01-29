from flask import Flask, jsonify, abort
from database import get_connection

app = Flask(__name__)

@app.route('/v1/movie/<int:record_id>', methods=['GET'])
def get_movie(record_id):
    """根据 record_id 获取电影信息"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
    movie = cursor.fetchone()
    connection.close()

    if not movie:
        abort(400, description="Movie not found")
    return jsonify({'movie': movie})

@app.route('/v1/healthcheck', methods=['GET'])
def healthcheck():
    """检查数据库连接状态"""
    try:
        connection = get_connection()
        connection.close()
        return jsonify({'status': 'healthy'})
    except:
        abort(503, description="Database connection failed")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

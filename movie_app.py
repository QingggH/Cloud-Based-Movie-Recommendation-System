from flask import Flask, jsonify, make_response, request, Response
import jwt
import datetime
import mysql.connector
from functools import wraps
from database import get_connection
from collections import OrderedDict
import json

app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'


def create_response(data, status_code=200):
    if isinstance(data, dict):  
        data = OrderedDict(data)
    json_data = json.dumps(data, ensure_ascii=False)  
    response = Response(json_data, status=status_code, content_type="application/json")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return create_response({"error": "Token is missing!"}, 401)

        try:
            token = token.replace("Bearer ", "")
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['email']
        except:
            return create_response({"error": "Token is invalid!"}, 401)

        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/v1/register", methods=["POST"])
def register():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return create_response({"error": "Missing email or password"}, 400)

    email = data["email"]
    password = data["password"]  

    return create_response({"message": "User registered successfully"}, 201)


@app.route("/v1/login", methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get("email") or not auth.get("password"):
        return create_response({"error": "Missing email or password"}, 400)

    
    token = jwt.encode({
        "email": auth["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return create_response({"token": token}, 200)


@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    if request.args:
        return create_response({"error": "Bad Request"}, 400)

    try:
        connection = get_connection()
        if connection.is_connected():
            connection.close()
            return create_response({"status": "OK"}, 200)
        return create_response({"error": "Service Unavailable"}, 503)
    except:
        return create_response({"error": "Service Unavailable"}, 503)


@app.route("/v1/healthcheck", methods=["POST", "PUT", "DELETE", "PATCH"])
def healthcheck_invalid():
    return create_response({"error": "Bad Request"}, 400)


@app.route("/v1/movie", methods=["GET"])
@app.route("/v1/movie/<int:movie_id>", methods=["GET"])
@token_required
def get_movie(current_user, movie_id=None):
    if movie_id is None:
        movie_id = request.args.get("id")
        if not movie_id or not movie_id.isdigit():
            return create_response({"error": "Invalid or missing movie ID"}, 400)
        movie_id = int(movie_id)

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT m.movieId, m.title, GROUP_CONCAT(g.genre) AS genres 
        FROM movies m 
        LEFT JOIN movies_genres mg ON m.movieId = mg.movieId 
        LEFT JOIN genres g ON mg.genreId = g.genreId 
        WHERE m.movieId = %s 
        GROUP BY m.movieId
    """, (movie_id,))

    movie = cursor.fetchone()
    connection.close()

    if movie:
        genres_list = movie["genres"].split(",") if movie["genres"] else []
        response_data = OrderedDict([
            ("movieId", movie["movieId"]),
            ("title", movie["title"]),
            ("genres", genres_list)  # `genres` 确保在最后
        ])
        return create_response(response_data, 200)

    return create_response(OrderedDict([
        ("error", "Movie not found")
    ]), 404)


@app.route("/v1/rating/<int:movie_id>", methods=["GET"])
@token_required
def get_rating(current_user, movie_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT AVG(rating) AS average_rating FROM ratings WHERE movieId = %s", (movie_id,))
    rating = cursor.fetchone()
    connection.close()

    if rating and rating["average_rating"] is not None:
        response_data = OrderedDict([
            ("movieId", movie_id),
            ("average_rating", float(rating["average_rating"]))
        ])
        return create_response(response_data, 200)

    return create_response({"error": "No ratings found for this movie"}, 404)



@app.route("/v1/link/<int:movie_id>", methods=["GET"])
@token_required
def get_link(current_user, movie_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT imdbId, tmdbId FROM links WHERE movieId = %s", (movie_id,))
    link = cursor.fetchone()
    connection.close()

    if link:
        response_data = OrderedDict([
            ("movieId", movie_id),
            ("imdbId", link["imdbId"]),
            ("tmdbId", link["tmdbId"])
        ])
        return create_response(response_data, 200)

    return create_response({"error": "No links found for this movie"}, 404)



@app.errorhandler(401)
def unauthorized(error):
    return create_response({"error": "Unauthorized"}, 401)

#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
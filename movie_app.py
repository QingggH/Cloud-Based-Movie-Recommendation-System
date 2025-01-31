from flask import Flask, jsonify, make_response, request
import mysql.connector
from database import get_connection

app = Flask(__name__)

def create_response(data, status_code=200):
    """Generate a consistent JSON response."""
    return make_response(jsonify(data), status_code)

@app.after_request
def add_no_cache_header(response):
    """Ensure all responses include a no-cache header."""
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    """Check the database connection status."""
    if request.args or request.form:
        return create_response({"error": "Bad Request"}, 400)

    try:
        connection = get_connection()
        if connection and connection.is_connected():
            connection.close()
            return create_response({"status": "OK"}, 200)
        else:
            return create_response({"error": "Service Unavailable"}, 503)
    except mysql.connector.Error:
        return create_response({"error": "Service Unavailable"}, 503)
    except Exception:
        return create_response({"error": "Service Unavailable"}, 503)

@app.route("/v1/movie/<int:record_id>", methods=["GET"])
def get_movie(record_id):
    """Retrieve movie details based on record_id."""
    connection = None
    cursor = None

    try:
        connection = get_connection()
        if not connection or not connection.is_connected():
            return create_response({"error": "Service Unavailable"}, 503)

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE movieId = %s", (record_id,))
        movie = cursor.fetchone()

        if movie:
            ordered_movie = {
                "movieId": movie["movieId"],
                "title": movie["title"],
                "genres": movie["genres"]
            }
            return create_response({"movie": ordered_movie}, 200)
        else:
            return create_response({"error": "Bad Request"}, 400)

    except mysql.connector.Error:
        return create_response({"error": "Service Unavailable"}, 503)
    except Exception:
        return create_response({"error": "Service Unavailable"}, 503)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors."""
    return create_response({"error": "Bad Request"}, 400)

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed errors."""
    return create_response({"error": "Bad Request"}, 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

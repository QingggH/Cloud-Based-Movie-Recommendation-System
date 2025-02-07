from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

# Add no-cache headers to responses
@app.after_request
def set_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# Health check route
@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    if request.args or request.form:  # Check for any parameters
        return make_response(jsonify({"error": "Bad Request"}), 400)
    return "", 200  # Return an empty response with 200 OK

# Global error handler for unsupported methods or routes
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({"error": "Bad Request"}), 400)

# Explicitly handle invalid methods for /v1/healthcheck
@app.route("/v1/healthcheck", methods=["POST", "PUT", "DELETE", "PATCH"])
def invalid_method():
    return make_response(jsonify({"error": "Bad Request"}), 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

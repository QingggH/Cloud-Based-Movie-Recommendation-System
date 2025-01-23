from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

# Add no-cache headers to responses
@app.after_request
def set_cache_control(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# Health check route
@app.route("/v1/healthcheck", methods=["GET"])
def check_health():
    if request.values:  
        return make_response(jsonify({"error": "Bad Request"}), 400)

    return jsonify({"status": "OK"}), 200

# Global error handler
def handle_bad_request(error):
    return jsonify({"error": "Bad Request"}), 400

app.register_error_handler(404, handle_bad_request)
app.register_error_handler(405, handle_bad_request)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

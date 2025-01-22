from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.after_request
def add_no_cache_header(response):
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.route("/v1/healthcheck", methods=["GET"])
def healthcheck():
    if request.args or request.form:
        return make_response(jsonify({"error": "Bad Request"}), 400)

    return make_response(jsonify({"status": "OK"}), 200)

@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({"error": "Bad Request"}), 400)

@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(jsonify({"error": "Bad Request"}), 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
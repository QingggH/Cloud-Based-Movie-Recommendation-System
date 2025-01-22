from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/v1/healthcheck', methods=['GET'])
def healthcheck():
    # Check if there are query parameters
    if request.args:
        return '', 400  # Return 400 Bad Request if parameters are present
    return '', 200  # Return 200 OK if the request is successful

@app.errorhandler(405)
def method_not_allowed(e):
    # Return 400 Bad Request for unsupported methods
    return '', 400

@app.after_request
def add_headers(response):
    # Add required headers to all responses
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    # Run the server on localhost:8080
    app.run(host='0.0.0.0', port=8080)

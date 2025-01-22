from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/v1/healthcheck', methods=['GET'])
def healthcheck():
    if request.args:
        return make_response(jsonify({'error': 'Bad Request'}), 400)
    
    response = make_response(jsonify({'status': 'OK'}), 200)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/v1/healthcheck', methods=['POST', 'PUT', 'DELETE', 'PATCH'])
def healthcheck_invalid_methods():
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(405)
def method_not_allowed_error(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
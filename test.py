from flask import Flask, jsonify, request, make_response
app = Flask(__name__)
@app.route('/v1/healthcheck', methods=['GET'])
def healthcheck():
    if request.args:
        return make_response(jsonify(), 400)
    
    response = make_response(jsonify(), 200)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
@app.errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
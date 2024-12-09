from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' key in request"}), 400
    
    query = data['query']
    print('Query:', query)
    
    # TODO: get response using query

    response = query
    
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)

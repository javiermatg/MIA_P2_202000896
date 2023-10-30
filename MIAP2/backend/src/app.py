from flask import Flask, jsonify, request
from flask_cors import CORS  
from getData import getData

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api-execute', methods=['POST'])
def execute():
    data = request.get_json()
    entry_value = data.get('entry')
    response = getData(entry_value)
    return jsonify( {'salida': response})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port= 8000)
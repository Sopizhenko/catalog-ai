from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint working"})

@app.route('/api/companies', methods=['GET'])
def get_companies():
    try:
        with open('data/companies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Test Flask App...")
    app.run(debug=True, host='0.0.0.0', port=5000)

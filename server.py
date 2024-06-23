from flask import Flask, jsonify
import requests
app = Flask(__name__)

@app.route('/run-function', methods=['POST'])
def run_function():
    data = {"message": "Function execution triggered"}
    try:
        response = requests.post('http://localhost:5001/receive-data', json=data)
        if response.status_code == 200:
            return jsonify({"message": "Function execution triggered and data sent to Streamlit"})
        else:
            return jsonify({"message": "Failed to send data to Streamlit"}), 500
        
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True,port=5000)
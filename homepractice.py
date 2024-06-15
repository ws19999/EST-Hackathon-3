from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import streamlit as st
import requests

app = Flask(__name__)
CORS(app)

# Function to be called from HTML
def streamlit_function():
    st.write("Streamlit function executed!")

# Streamlit app
def streamlit_app():
    st.title("Streamlit and Flask Communication")
    
    if 'response_from_html' in st.session_state:
        st.write('Response from HTML:', st.session_state['response_from_html'])
    
    if st.button("Call Flask API"):
        response = requests.post("http://localhost:5000/start")
        if response.ok:
            st.session_state['response_from_html'] = response.json().get('message')
        else:
            st.session_state['response_from_html'] = "Failed to get response from Flask API."

# Flask endpoint to handle button click
@app.route('/start', methods=['POST'])
def start():
    streamlit_function()
    response_data = {"message": "Streamlit function executed."}
    return jsonify(response_data)

# Run Flask app in a separate thread
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    # Run Flask server in the background
    thread = Thread(target=run_flask)
    thread.start()
    
    # Run Streamlit app
    streamlit_app()

import streamlit as st
import streamlit.components.v1 as components
from flask import Flask, request, jsonify
import threading
import time
import requests

st.set_page_config(layout="wide")

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# Load HTML content
html_file_path = '2.landing1_1_.html'
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Streamlit interface setup
hide_sidebar()
components.html(html_content, height=1300)

# Flask app setup
app = Flask(__name__)
data_storage = {
    "received_data": None,
    "switch_to_login": False
}

@app.route('/receive-data', methods=['POST'])
def receive_data():
    global data_storage
    data = request.json
    data_storage['received_data'] = data['message']
    data_storage['switch_to_login'] = True
    return jsonify({"status": "success", "message": "Data received"})

@app.route('/get-status', methods=['GET'])
def get_status():
    global data_storage
    return jsonify({
        "switch_to_login": data_storage['switch_to_login'],
        "message": data_storage['received_data']
    })

def run_flask():
    app.run(port=5001, debug=False, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

def check_flask_status():
    try:
        response = requests.get("http://localhost:5001/get-status")
        if response.status_code == 200:
            data = response.json()
            return data.get("switch_to_login", False), data.get("message", None)
        else:
            return False, None
    except requests.exceptions.RequestException as e:
        st.error(f"Error checking Flask status: {e}")
        return False, None

def reset_flask_status():
    global data_storage
    data_storage['switch_to_login'] = False
    data_storage['received_data'] = None

while True:
    switch_to_login, received_data = check_flask_status()
    
    if switch_to_login:
        reset_flask_status()
        switch_to_login=False
        if 'username' in st.session_state:
            st.switch_page('pages/chatbot.py')
        else:
            st.switch_page('pages/login.py')
    
    if received_data is not None:
        st.session_state['data'] = received_data
        st.experimental_rerun()
    
    time.sleep(1)  # Add a short delay to prevent tight loop

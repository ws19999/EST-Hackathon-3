import mysql.connector
import streamlit as st
from openai import OpenAI
from st_chat_message import message

# 세션 상태에서 사용자 아이디 가져오기
username = st.session_state.get('username')

# MySQL 데이터베이스에 연결하는 함수
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="admins"
    )

# 대화 저장 함수
def save_chat(user_message, bot_response, words):
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = username  # 사용자 이름을 테이블 이름으로 사용
    cursor.execute(f"INSERT INTO {table_name} (user_message, bot_response, words) VALUES (%s, %s, %s)", (user_message, bot_response, words))
    conn.commit()
    conn.close()

# 대화 불러오기 함수
def load_chat_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    table_name = username  # 사용자 이름을 테이블 이름으로 사용
    cursor.execute(f"SELECT user_message, bot_response, timestamp FROM {table_name} ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return [{"role": "user", "content": user_message} if i % 2 == 0 else {"role": "assistant", "content": bot_response} for i, (user_message, bot_response, _) in enumerate(rows)]
# openai API 키 인증
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("당신의 친구")
#st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history()

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat(prompt, "", "")  # 빈 bot_response와 words로 저장
    message(prompt, is_user=True)
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    words = " ".join(msg.split())  # 예시로 단어를 결합하여 words 필드를 채움
    st.session_state.messages.append({"role": "assistant", "content": msg})
    save_chat(prompt, msg, words)
    message(msg, is_user=False)

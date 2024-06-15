import mysql.connector
import streamlit as st
from openai import OpenAI
from st_chat_message import message
def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()
# 사용자 이름 설정
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
    return [{"role": "user", "content": user_message} if bot_response=='' else {"role": "assistant", "content": bot_response} for i, (user_message, bot_response, _) in enumerate(rows)]

# openai API 키 인증
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("마음들이")
#st.caption("힘들고 지친 당신의 친구가 되어줍니다")

if "messages" not in st.session_state:
    st.session_state["messages"] = load_chat_history()
    if st.session_state['messages']==[]:
        st.session_state.messages.append({"role": "system", "content": "You are a friendly and polite assistant. Always respond in a kind and helpful manner. Ask questions to learn about themselves"})
        st.session_state["messages"].append({"role": "assistant", "content": "안녕? 만나서 반가워 "})
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
        model="ft:gpt-3.5-turbo-1106:personal:ourchatbot:9a5TUFUx", 
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    words = " ".join(msg.split())  # 예시로 단어를 결합하여 words 필드를 채움
    st.session_state.messages.append({"role": "assistant", "content": msg})
    save_chat('', msg, words)
    message(msg, is_user=False)
import mysql.connector
import streamlit as st
from openai import OpenAI
from st_chat_message import message
import random
temp=0
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
    
    if len(rows) > 50:
    # 삭제할 데이터의 타임스탬프를 가져오기
        cursor.execute(f"""
        SELECT timestamp FROM {table_name}
        ORDER BY timestamp DESC
        LIMIT 1 OFFSET 49
        """)
        timestamp_to_keep = cursor.fetchone()

        # 오래된 데이터 삭제
        if timestamp_to_keep:
            cursor.execute(f"DELETE FROM {table_name} WHERE timestamp < %s", (timestamp_to_keep[0],))
            conn.commit()

        # 삭제 후 남은 데이터 다시 가져오기
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
        st.session_state["messages"].append({"role": "assistant", "content": "오늘 당신의 기분은 어떠신가요?"})
    st.session_state.messages.append({"role": "system", "content": "You are a friendly and polite assistant. Always respond in a kind and helpful manner. Encourage the user to explore self-discovery and learn about themselves. Ask engaging questions that prompt self-reflection and personal insights."})
for msg in st.session_state.messages:
    if msg["role"]!="system":
        #num=random.randint(0, 10000)
        message(msg["content"], is_user=msg["role"] == "user",key = f"{temp}")
        temp+=1

def extract_keywords(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract important keywords from the following prompt:\n\n{prompt}\n\nKeywords:"}
        ],
        max_tokens=10
    )
    keywords = response.choices[0].message.content.strip()
    return keywords

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 중요한 단어 추출
    important_words = extract_keywords(prompt)
    save_chat(prompt, "", important_words)  # 빈 bot_response와 words로 저장
    #num=random.randint(0, 10000)
    
    message(prompt, is_user=True,key = f"{temp}")
    
    
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:ourchatbot:9a5TUFUx", 
        messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    temp+=1
    message(msg, is_user=False,key = f"temp")
    st.session_state.messages.append({"role": "assistant", "content": msg})
    temp+=1
    save_chat('', msg,'')
    #num=random.randint(0, 10000)
    
    
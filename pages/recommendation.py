import streamlit as st
import mysql.connector
from openai import OpenAI

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()

test_score=st.session_state['score'] #이전 테스트 값

# MySQL 데이터베이스에 연결하는 함수
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
            user="user",
            password="password",
            database="admins"
    )

# 제목 및 설명
st.title("마음들이 커뮤니티 추천")
st.write("당신의 감정 상태에 맞는 커뮤니티를 추천드려요!")
st.session_state['username']='test'
username = st.session_state.get('username')


# openai API 키 인증
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

conn = get_db_connection()
cursor = conn.cursor()
table_name = username  # 사용자 이름을 테이블 이름으로 사용
cursor.execute(f"SELECT words FROM {table_name} ")
rows = cursor.fetchall()
st.session_state.messages=[]
for data in rows:
    for word in data:
        st.session_state.messages.append({"role": "user", "content": f'word'})
response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal:ourchatbot:9a5TUFUx", #파인튜닝한 모델
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"우울 , 무기력, 상실감, 외로움 에 가까우면 1, 슬픔,분노,감정조절이상 에 가까우면 2, 다 아니면 0을 대답하세요"}
        ],
        max_tokens=1
    )

if response:
    # 감정 상태 판단
    if response.choices[0].message.content == 0:
        emotion = "긍정적"
        communities = ["긍정 에너지 커뮤니티", "행복 나누기", "감사일기"]
    elif response.choices[0].message.content == 1:
        emotion = "우울,외로움"
        if(test_score>=10):
            communities = ["사회적 고립 모임", "위로와 공감", "우울증 극복"]
        else:
            communities = ["우울증 모임", "위로와 공감", "우울증 극복"]
    else:
        emotion = "감정 조절 이상"
        if(test_score>=10):
            communities = ["대인관계 불안 모임", "휴식", "산책"]
        else:
            communities = ["스트레스 모임", "기분 전환용 운동"]

    # 결과 출력
    st.write(f"당신의 감정 상태는 **{emotion}**인 것 같습니다.")
    st.write("추천하는 커뮤니티 및 활동:")
    for community in communities:
        st.write(f"- {community}을 추천드립니다")
else:
    st.write("챗봇이랑 대화하고 질문지 검사를 해보는건 어떤가요!")
if(st.button('홈화면으로')):
    st.session_state['messages'].clear()
    st.switch_page('homepage.py')

st.markdown("""
<style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stTextInput input {
        border-radius: 12px;
        border: 2px solid #4CAF50;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

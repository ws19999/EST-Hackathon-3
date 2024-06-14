import streamlit as st
import mysql.connector
import hashlib

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()
# MySQL 데이터베이스 연결 설정
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
            user="user",
            password="password",
            database="admins"
    )

# 로그인 기능
def login():
    st.title("아자아자 화이팅!!!")

    # 사용자 입력 받기
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # 로그인 버튼 클릭 여부 확인
    if st.button("Login"):
        # 비밀번호 해시화
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # SQL 쿼리 실행
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Incorrect username or password. Please try again.")

        cursor.close()
        connection.close()

    st.page_link("pages/join.py", label="회원가입")

# 로그인 함수 호출
login()
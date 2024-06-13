import streamlit as st
import mysql.connector

# MySQL 데이터베이스 연결 설정
mydb = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mydatabase"
)

# MySQL 커서 생성
cursor = mydb.cursor()

# 사용자 테이블 생성 (한 번만 실행하면 됨)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

# 회원가입 기능
def signup():
    st.title("Sign Up")

    # 사용자 입력 받기
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # 회원가입 버튼 클릭 여부 확인
    if st.button("Sign Up"):
        # 사용자 이름 중복 확인
        cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        user = cursor.fetchone()

        if user:
            st.error("Username already exists. Please choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            # 새로운 사용자 추가
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))
            mydb.commit()
            st.success("You have successfully signed up. Please proceed to login.")

# 회원가입 함수 호출
signup()

# MySQL 연결 종료 (애플리케이션 종료 시)
def on_app_close():
    cursor.close()
    mydb.close()

st.on_event('app_end', on_app_close)

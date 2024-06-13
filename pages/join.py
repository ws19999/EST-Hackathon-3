import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

# MySQL 데이터베이스 연결 설정
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",
            database="admins" 
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# 비밀번호 해싱 함수
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 회원가입 기능
def signup():
    st.title("Sign Up")

    # 사용자 입력 받기
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # 회원가입 버튼 클릭 여부 확인
    if st.button("Sign Up"):
        if not new_username or not new_password or not confirm_password:
            st.error("All fields are required.")
            return

        conn = get_db_connection()
        if conn is None:
            return

        cursor = conn.cursor()

        # 사용자 이름 중복 확인
        cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        user = cursor.fetchone()

        if user:
            st.error("Username already exists. Please choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            # 새로운 사용자 추가
            hashed_password = hash_password(new_password)
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
                conn.commit()
                st.success("You have successfully signed up. Please proceed to login.")
            except Error as e:
                st.error(f"Failed to sign up: {e}")
        
        cursor.close()
        conn.close()

# 사용자 테이블 생성 함수
def create_users_table():
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# 사용자 테이블 생성 호출
create_users_table()

# 회원가입 함수 호출
signup()

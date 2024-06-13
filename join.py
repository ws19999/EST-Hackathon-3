import streamlit as st

# 더미 사용자 데이터베이스
dummy_users = {}

# 회원가입 기능
def signup():
    st.title("Sign Up")

    # 사용자 입력 받기
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # 회원가입 버튼 클릭 여부 확인
    if st.button("Sign Up"):
        if new_username in dummy_users:
            st.error("Username already exists. Please choose another one.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        else:
            # 새로운 사용자 추가
            dummy_users[new_username] = new_password
            st.success("You have successfully signed up. Please proceed to login.")

# 회원가입 함수 호출
signup()

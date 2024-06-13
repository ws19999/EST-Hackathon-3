import streamlit as st

# 더미 사용자 데이터
dummy_users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# 로그인 기능
def login():
    st.title("아자아자 화이팅!!!")

    # 사용자 입력 받기
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # 로그인 버튼 클릭 여부 확인
    if st.button("Login"):
        if username in dummy_users:
            if password == dummy_users[username]:
                st.success(f"Welcome back, {username}!")
            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.error("User not found. Please try again.")

    st.page_link("pages/join.py", label = "회원가입" )

# 로그인 함수 호출
login()

import streamlit as st
import mysql.connector
from mysql.connector import Error
from PIL import Image
import requests
from io import BytesIO

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()


# 이미지 URL
#url = ''

# 이미지 다운로드
#response = requests.get(url)
#img = Image.open(BytesIO(response.content))


# 로그인 기능
def first():
    # 이미지 표시
    st.image('https://cdn.pixabay.com/photo/2020/08/05/13/27/eco-5465461_640.png',caption='로고자리?')
    st.title("sample app")
    st.image('https://images.unsplash.com/photo-1545169128-53e46e195d46?q=80&w=1976&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',caption='애니메이션이나 기타 이미지자리')
    st.page_link("pages/login.py", label="로그인")
    st.page_link("pages/join.py", label="회원가입")

# 로그인 함수 호출
first()
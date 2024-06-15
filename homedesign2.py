import streamlit as st
import streamlit.components.v1 as components

# HTML 파일을 읽어와서 내용 저장
html_file_path = '2.landing1_1_.html'
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Streamlit의 전체 화면 너비 사용 설정
st.set_page_config(layout="wide")

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()
# URL 경로에 따라 다른 화면을 보여줍니다.
page = st.query_params.get('page', [''])[0]

if page == 'next_page':
    st.query_params(page='') 
    st.switch_page("pages/login.py")
    
# Streamlit에서 HTML 내용을 렌더링
else:
    components.html(html_content, height=1300)


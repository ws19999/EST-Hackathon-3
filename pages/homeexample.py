import streamlit as st

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
hide_sidebar()

# 세션 상태에서 사용자 아이디 가져오기
username = st.session_state.get('username')

st.title("메인 페이지")
st.write(f"안녕하세요, {username}님!")

st.page_link("pages/gptpractice2.py", label="gpt")


if __name__ == "__main__":
    hide_sidebar()

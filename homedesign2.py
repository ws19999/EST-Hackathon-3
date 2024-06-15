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
#components.html(html_content, height=1300)


# 세션 상태 초기화
if 'message' not in st.session_state:
    st.session_state['message'] = "No message yet"

# JavaScript 메시지 처리
def on_message_received(message):
    st.session_state['message'] = message
    st.session_state['message']
    st.experimental_rerun()

# JavaScript 이벤트 리스너 추가
js_code = """
<script>
    window.addEventListener("message", (event) => {
        if (event.origin !== window.location.origin) {
            return;
        }
        const message = event.data;
        const streamlitMessageEvent = new CustomEvent("streamlit:message", {
            detail: message
        });
        window.dispatchEvent(streamlitMessageEvent);
    });
</script>
"""

# HTML 렌더링
components.html(html_content + js_code, height=600, scrolling=True)

# Streamlit의 Custom Event Listener
st.write("Received message:", st.session_state['message'])
print(st.session_state['message'])

# JavaScript 이벤트를 Streamlit으로 전달
components_code = """
<script>
    const streamlitMessageEvent = new CustomEvent("streamlit:message", {
        detail: (msg) => {
            const pythonHandler = window.streamlitEventMessage;
            if (pythonHandler) {
                pythonHandler({detail: msg});
            }
        }
    });

    window.streamlitEventMessage = function(event) {
        const message = event.detail;
        Streamlit.setComponentValue(message);
    };
</script>
"""

components.html(components_code, height=0)

# 메시지 핸들러
def message_handler(msg):
    st.session_state['message'] = msg
    st.session_state['message']
    st.experimental_rerun()

st.write("Received message:", st.session_state['message'])
st.session_state['message']
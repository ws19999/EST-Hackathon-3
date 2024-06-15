from openai import OpenAI
import streamlit as st
from st_chat_message import message

# openai API 키 인증
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("당신의 친구")
#st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕? 만나서 반가워"}]

for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    message(prompt, is_user=True)
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=st.session_state.messages
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    message(msg, is_user=False)

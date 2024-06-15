from openai import OpenAI
import streamlit as st
from st_chat_message import message

#openai API 키 인증
openai_api_key = st.secrets["OPENAI_API_KEY"]

#Set title and caption
st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

#Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕? 나는 챗봇이야. 너의 질문이 있니?"}]

#Display previous messages
for msg in st.session_state.messages:
    st.text(msg["content"])

#Receive user input (answer)
if answer := st.text_input("Answer the question:"):
    # Add user's answer to the messages
    st.session_state.messages.append({"role": "user", "content": answer})

    # Display user's answer
    st.text("User: " + answer)

    # Perform OpenAI API call to generate response
    # Assuming you have defined openai_api_key variable
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=st.session_state.messages
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})

    # Display assistant's response
    st.text("Assistant: " + msg)

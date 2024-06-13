import streamlit as st

# Page configuration
st.set_page_config(page_title="Multi-page Streamlit App", layout="centered")

# Dictionary to map button actions to pages
page_map = {
    "Page 1": "gptpractice.py",
    "Page 2": "gpt예시.py"
}

# Main function to display buttons and navigate to pages
def main():
    st.title("Welcome to the Multi-page App")

    # Button to navigate to Page 1
    if st.button("Go to Page 1"):
        #st.session_state.current_page = "Page 1"
        #st.rerun()
        st.switch_page("gptpractice.py")

    # Button to navigate to Page 2
    if st.button("Go to Page 2"):
        #st.session_state.current_page = "Page 2"
        #st.experimental_rerun()
        st.switch_page("gpt예시.py")

main()

from openai import OpenAI
import streamlit as st
from st_chat_message import message
from forms_question import questions, IC, calculate_score, interpret_scores

# OpenAI GPT-4o 모델 설정
client = OpenAI(api_key=openai_api_key)

# Streamlit 앱 생성
def main():
    st.title('MMPI-2-RF 검사 도구')
    st.markdown("""
    이 앱은 MMPI-2-RF 검사 도구를 시뮬레이션하는 데 사용됩니다. 아래의 각 문항에 대한 질문에 따라
    선택지를 골라주세요. 각 선택지는 4점 리커트 척도로 평가됩니다.
    """)

    # 문항 입력 섹션
    responses = {}
    for category, question_list in questions.items():
        st.subheader(f'{category.replace("_", " ").title()}')
        response_list = []
        for i, question in enumerate(question_list):
            response = st.radio(f'{i + 1}. {question}', options=[1, 2, 3, 4], index=1, key=f'{category}_{i}')
            if not response.isnumeric(): ## 내가 쓴것
                st.text('숫자로 쳐주세요') 
            response_list.append(response)
            
        responses[category] = response_list

    # 점수 계산
    scores = calculate_score(responses)

    # 해석
    interpretation = interpret_scores(scores)

    # 결과 출력
    st.subheader('검사 결과 해석')
    for category, result in interpretation.items():
        st.write(f'{category.replace("_", " ").title()}: {result}')

    # 대화 기능 추가
    st.subheader('봇과 대화하기')
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "안녕? 만나서 반가워"}]

    for msg in st.session_state.messages:
        message(msg["content"], is_user=msg["role"] == "user")

    if prompt := st.text_input("나:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        message(prompt, is_user=True)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}] + st.session_state.messages[-5:],  # 최근 5개 메시지만 사용
            max_tokens=50
        )
        
        msg = response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        message(msg, is_user=False)

if __name__ == '__main__':
    main()
import streamlit as st

questions = [
        "나는 대부분의 시간을 혼자 보내는 것이 좋다.",
        "나는 사람들과 어울리는 것이 불편하다.",
        "나는 사람들과 만나는 것을 피하는 경향이 있다.",
        "나는 낯선 사람들과 있으면 불편함을 느낀다.",
        "나는 사회생활보다는 혼자 있는 것이 더 편하다.",
    
        "나는 사회적 상황에서 긴장되고 불안을 느낀다.",
        "나는 사람들 앞에서 말하는 것이 두렵다.",
        "나는 다른 사람들의 반응에 지나치게 민감하다.",
        "나는 다른 사람들이 나를 어떻게 생각할지에 대해 늘 걱정한다.",
        "나는 새로운 사람들을 만나는 것에 대해 부담을 느낀다.",
    
        "나는 대인관계에서 종종 실망감을 경험한다.",
        "나는 다른 사람들에게 내 감정을 표현하는 것이 어렵다.",
        "나는 사람들과 깊이 있는 대화를 나누기 어려워한다.",
        "나는 사람들과의 관계에서 진실된 모습을 보이기 어려워한다.",
    
        "나는 다른 사람들로부터 비난받는 것에 대해 두려움을 느낀다.",
        "나는 사람들과의 갈등 상황을 피하고 싶어 한다.",
        "나는 다른 사람들과 함께 있을 때 내 자신을 잃어버릴 것 같은 느낌이 든다.",
    
        "나는 다른 사람들과 친밀한 관계를 맺는 것이 어렵다.",
        "나는 사람들과 대화를 시작하고 유지하는 것이 어렵다.",
        "나는 혼자 있을 때 가장 행복하고 안전함을 느낀다."
    ]

##################################################################

# Streamlit 앱의 타이틀 설정
st.title("MMPI-2-RF 검사")
st.markdown("""
    아래의 각 문항에 대한 질문에 따라 1,2,3,4 중 하나의 숫자를 입력하세요.
    """)

# 세션 상태 초기화: 메시지 기록을 저장할 리스트
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "MMPI-2-RF 검사 도구를 시작합니다."}]

# 이전 채팅 메시지 표시
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

responses = []
###########################################################
# Use a loop to generate unique keys for st.text_input

for idx, question in enumerate(questions, start=1):
    st.write(f"질문 {idx}: {question}")
    key = f"question_{idx}"  # Generate a unique key for each question
    prompt = st.text_input(f"점수 입력", key=key)
    
    if prompt:  # 입력값이 비어 있지 않을 때
        if prompt.isdigit():  # 입력값이 숫자인지 확인
            number = int(prompt)
            if 1 <= number <= 4:  # 숫자가 1에서 4 사이에 포함되는지 확인
                st.write(' ')
                responses.append(number)
            else:
                st.warning("숫자를 1에서 4 사이로 입력해주세요.")
                break  # 숫자가 유효하지 않으면 종료
        else:
            st.warning("숫자를 입력해주세요.")
            break  # 숫자가 아니면 종료
    # key_button = f"question_{idx}_button" 
    # if st.button("다음 질문으로 이동",key=key_button) or (prompt and (prompt.isdigit() and (1 <= int(prompt) <= 4))):
    #     continue
#################################################################3333
if responses:
    total_sum = sum(responses)
    st.write(f"총 점수: {total_sum}")
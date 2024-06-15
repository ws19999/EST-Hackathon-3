# MMPI-2-RF 문항 및 점수 해석 기준
def questions():
    que = {
        'social_isolation': [
            "나는 대부분의 시간을 혼자 보내는 것이 좋다.",
            "나는 사람들과 어울리는 것이 불편하다.",
            "나는 사람들과 만나는 것을 피하는 경향이 있다.",
            "나는 낯선 사람들과 있으면 불편함을 느낀다.",
            "나는 사회생활보다는 혼자 있는 것이 더 편하다."
        ],
    'interpersonal_anxiety': [
        "나는 사회적 상황에서 긴장되고 불안을 느낀다.",
        "나는 사람들 앞에서 말하는 것이 두렵다.",
        "나는 다른 사람들의 반응에 지나치게 민감하다.",
        "나는 다른 사람들이 나를 어떻게 생각할지에 대해 늘 걱정한다.",
        "나는 새로운 사람들을 만나는 것에 대해 부담을 느낀다."
    ],
    'emotional_constriction': [
        "나는 대인관계에서 종종 실망감을 경험한다.",
        "나는 다른 사람들에게 내 감정을 표현하는 것이 어렵다.",
        "나는 사람들과 깊이 있는 대화를 나누기 어려워한다.",
        "나는 사람들과의 관계에서 진실된 모습을 보이기 어려워한다."
    ],
    'interpersonal_avoidance': [
        "나는 다른 사람들로부터 비난받는 것에 대해 두려움을 느낀다.",
        "나는 사람들과의 갈등 상황을 피하고 싶어 한다.",
        "나는 다른 사람들과 함께 있을 때 내 자신을 잃어버릴 것 같은 느낌이 든다."
    ],
    'withdrawn_preferential': [
        "나는 다른 사람들과 친밀한 관계를 맺는 것이 어렵다.",
        "나는 사람들과 대화를 시작하고 유지하는 것이 어렵다.",
        "나는 혼자 있을 때 가장 행복하고 안전함을 느낀다."
    ]
}
    return que


# MMPI-2-RF 점수 해석 기준
def IC():
    interpretation_criteria = {
        'social_isolation': {15: "잠재적 위험", 20: "고위험군"},
        'interpersonal_anxiety': {15: "잠재적 위험", 20: "고위험군"},
        'emotional_constriction': {12: "잠재적 위험", 16: "고위험군"},
        'interpersonal_avoidance': {9: "잠재적 위험", 12: "고위험군"},
        'withdrawn_preferential': {9: "잠재적 위험", 12: "고위험군"}   
            }
    return interpretation_criteria

def calculate_score(responses):
    scores = {
        'social_isolation': sum(responses['social_isolation']),
        'interpersonal_anxiety': sum(responses['interpersonal_anxiety']),
        'emotional_constriction': sum(responses['emotional_constriction']),
        'interpersonal_avoidance': sum(responses['interpersonal_avoidance']),
        'withdrawn_preferential': sum(responses['withdrawn_preferential'])
    }
    return scores

def interpret_scores(scores):
    interpretation = {}
    for category, score in scores.items():
        for threshold, label in IC[category].items():
            if score >= threshold:
                interpretation[category] = label
                break  # 해당 카테고리는 이미 최소 임계치를 넘었으므로 더 이상 비교할 필요 없음
    return interpretation

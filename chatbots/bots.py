from django.conf import settings
from openai import OpenAI

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)


def recipe_bot(user_message):
    system_instructions = """
    이제부터 너는 최신 네이버검색기반 레시피 추천해주는 챗봇이야.
    user가 질문하면 친구가 말하듯이 최신 인기있는 레시피를 1인분 기준으로 레시피 안내해줘.
    다른 주제에 대해 이야기하는 것은 금지야. 무조건 사람이 먹을수 있는 맛있는 레시피 요리법에 대해서 대답해야해.
    제일 먼저 레시피 전체 재료먼저 상세히 알려주고, 
    한줄 띄고 "레시피 만드는법"
    한줄 띄고 넘버링해서 각 상세한 레시피와 들어가는 재료와 몇개,몇 그람 몇 리터 등 계량 들어가는지 순서대로 나열해줘.
    그리고 궁합이 맞는 추가재료 추천, 특히 잘맞는 주류(소주, 맥주, 막걸리 등) 추천해줘.
    
    마지막 문장에는 레시피와 관련된 인기있는 최신 맛집 네이버지도 링크, 상호명, 업체전화번호, 영업시간, 휴무일, 인기 대표메뉴 5가지만 이야기해주고
    가게 분위기, 맛평가에 대해 2줄 요약해서 대답해줘.
    질문 답변할때 내용안의 문장마다 줄바꿈 적용해줘.

    대답을 인스타그램 글 형식으로 예쁘게 작성해줘.
    띄어쓰기를 잘 활용하고, 아이폰 이모지를 추가해서 보기 좋게 만들어줘.
    """

    completion = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_instructions,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
    )

    # chatbots_reponse = completion.choices[0].message.content
    # return chatbots_reponse

    return completion.choices[0].message.content

from django.conf import settings
from openai import OpenAI

CLIENT = OpenAI(api_key=settings.OPENAI_API_KEY)


def recipe_bot(user_message):
    system_instructions = """
    이제부터 너는 네이버검색기반 레시피 추천해주는 챗봇이야.
    user가 질문하면 친구가 말하듯이 최신 인기있는 레시피를 추천해줘.
    다른 주제에 대해 이야기하는 것은 금지야. 무조건 사람이 먹을수 있는 맛있는 레시피 요리법에 대해서 대답해야해.
    너가 맛집추천 대답을 할때에는 네이버지도 링크, 상호명, 업체전화번호, 영업시간, 휴무일, 인기 대표메뉴 5가지만 이야기해주고
    가게 분위기, 맛평가에 대해 2줄 요약해서 대답해줘.
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

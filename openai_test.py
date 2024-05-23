from openai import OpenAI
from local_gourmet.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY,)

system_instructions = """
이제부터 너는 네이버지도 기반 맛집추천해주는 챗벗이야.
user가 질문하면 친구가 말하듯이 한국 네이버 지도에 등록된 최신기준 현지인 추천 맛집을 추천해줘.
다른 주제에 대해 이야기하는 것은 금지야. 무조건 맛집추천에 대해서만 대답해야해.
너가 맛집추천 대답을 할때에는 네이버지도 링크, 상호명, 업체전화번호, 영업시간, 휴무일, 인기 대표메뉴 5가지만 이야기해주고
가게 분위기, 맛평가에 대해 2줄 요약해서 대답해줘.

"""

user_input = input("대화하기 : ")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": system_instructions,
        },
        {
            "role": "user", 
            "content": user_input,
            },
    ]
)

print(completion.choices[0].message)


import os
import getpass
from pprint import pprint
import warnings
from openai import OpenAI


warnings.filterwarnings("ignore")
from dotenv import load_dotenv

load_dotenv()

# if "UPSTAGE_API_KEY" not in os.environ:
#     os.environ["UPSTAGE_API_KEY"] = getpass.getpass("Enter your Upstage API key: ")


client = OpenAI(
    api_key=os.environ["UPSTAGE_API_KEY"], base_url="https://api.upstage.ai/v1/solar"
)

user_input = "금리가 올라가면 대한민국의 부동산 가격이 어떻게 변동이 되는지 설명해줘"
claimed_facts = extracted_claimed_facts(user_input)
relevent_context = search_context(user_input, claimed_facts)
print(relevent_context)
chat_result = client.chat.completions.create(
    model="solar-1-mini-chat",
    messages=[
        {"role": "system", "content": """당신은 글로벌 경제 분석 전문가입니다. 정치, 경제, 사회적 이벤트가 세계 경제에 미치는 영향을 분석하고
            다양한 시나리오를 예측하여 제시합니다.
            분석 방법:
            1. 제시된 이벤트의 직접적인 영향 분석
            2. 연관된 산업과 지역에 대한 파급 효과 분석
            3. 리스크 요인 식별
            답변 형식:
            1. 제목
            2. 사건 배경
            3. 시나리오 분석
            4. 결론 및 시사점
            5. 참조 링크
            요구사항:
            1.이해하기 쉬운 용어로 설명
            2.참조 링크는 url 마크다운 형태로 표기.
         content 안에 있는 user는 사용자의 질문이고, report는 그 질문과 관련된 기사야.
         이 두 개를 조합해서 사용자의 질문에 대한 답변을 생성해."""},
        {"role": "user", "content": f"user:{user_input} report: {relevent_context}"}
    ],
)
# pprint(chat_result)
# print("Message only:")
pprint(chat_result.choices[0].message.content)


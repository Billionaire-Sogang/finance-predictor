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
        {"role": "system", "content": """사용자가 제시한 질문에 답변할 때, 주어진 뉴스 기사 내용을 참고해 구체적인 분석을 제공하라. 
         예를 들어, ‘트럼프 재집권 시 한국 경제에 미칠 영향’을 묻는 경우, 기사에 언급된 트럼프의 주요 경제 정책, 외교적 기조, 대외 무역 정책을 
         바탕으로 한국 경제에 미칠 잠재적 긍정적·부정적 영향을 평가하라. 특히 트럼프 전 대통령의 재집권이 한국의 수출입 환경, 외환시장, 외교 관계, 
         그리고 한국 산업에 끼칠 영향을 예측하여 다양한 관점에서 설명하라. 한국의 경제 이슈와 연관된 구체적 사례와 통계 자료를 활용하여 답변을 풍부하게 하고, 
         기사 내용이 다루지 않은 부분에 대해 추가적 맥락이나 설명을 제공하라. content 안에 있는 user는 사용자의 질문이고, report는 그 질문과 관련된 기사야.
         이 두 개를 조합해서 사용자의 질문에 대한 답변을 생성해."""},
        {"role": "user", "content": f"user:{user_input} report: {relevent_context}"}
    ],
)
# pprint(chat_result)
# print("Message only:")
pprint(chat_result.choices[0].message.content)
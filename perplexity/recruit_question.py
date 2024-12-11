from openai import OpenAI

# PPLX API 키 설정
PPLX_API_KEY = "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"

messages = [
    {
        "role": "system",
        "content": (
            "You are an artificial intelligence assistant and you need to "
            "engage in a helpful, detailed, polite conversation with a user."
        ),
    },
    {   
        "role": "user",
        "content": (
            "2024년도 삼성전자 DS부문 신입사원 채용공고를 검색해줘"
        ),
    },
]

client = OpenAI(api_key=PPLX_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="llama-3.1-sonar-small-128k-online",
    messages=messages,
)

# 응답에서 첫 번째 메시지의 내용을 가져와 출력
if response.choices:
    answer = response.choices[0].message.content
    print(answer)
else:
    print("error")


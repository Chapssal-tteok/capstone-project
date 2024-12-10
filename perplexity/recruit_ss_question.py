import requests

url = "https://api.perplexity.ai/chat/completions"

payload = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "Be precise and concise."
        },
        {
            "role": "user",
            "content": "삼성전자의 2024년도 SW 신입사원 채용공고를 보여줘"
        }
    ],
    "max_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
    "return_images": False,
    "return_related_questions": False,
    "frequency_penalty": 1,
    "search_recency_filter": "month",
    "presence_penalty": 0
}
headers = {
    # api key 보안 필요
    "Authorization": "Bearer [api-key]",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
#print(response.json()['choices'][0]['message']['content'] )
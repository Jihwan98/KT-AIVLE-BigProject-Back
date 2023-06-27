import openai
from settings_params import openai_apiKey

openai.api_key = openai_apiKey

def chatGPT(conf, disease):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"반려견 피부질환 AI model이 {conf}%의 Confidence로 [{disease}]을/를 예상하고있어.\n이 병명에 대해서 간단한 설명을 해줘.",
        temperature=0.4,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].text
import openai
from settings_params import openai_apiKey

openai.api_key = openai_apiKey

def chatGPT_disease(conf, disease):
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

def chatGPT_answer(disease, conf, title, contents):
    prompt = f"""반려견 피부질환 AI 진단결과와 함께 아래와 같은 내용으로 질문을 했다. 이에 알맞은 대답을 해줘.

AI 모델 진단 결과 : {conf}%의 Confidence로 [{disease}]을/를 예상
질문 제목 : {title}
질문 내용 : {contents}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content
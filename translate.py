from openai import OpenAI
from datasets import load_dataset
import pandas as pd
from dotenv import load_dotenv
import os


def translate_to_korean(client, text):
    """
    영어 텍스트를 한국어로 번역합니다.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a translator that translates English to Korean."},
                {"role": "user", "content": f"Translate this to Korean: {text}"}
            ]
        )
        translation = completion.choices[0].message.content.strip()
        return translation
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

def process_dataset(client, dataset_name):
    # Hugging Face 데이터셋 로드
    dataset = load_dataset(dataset_name, split="train")

    translated_data = []

    for i, data in enumerate(dataset):
        translated_row = {}
        for key, value in data.items():
            if isinstance(value, str):
                print(f"Translating {key} ({i+1}): {value[:50]}...")  # 첫 50자만 출력
                translated_row[key] = translate_to_korean(client, value)
            else:
                translated_row[key] = value
        translated_data.append(translated_row)

    # 번역된 데이터를 DataFrame으로 변환
    df = pd.DataFrame(translated_data)

    # 파일 저장 (데이터셋 이름 기반)
    output_file = f"translated_{dataset_name.replace('/', '_')}.csv"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Translated dataset saved to {output_file}")


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key : 
    client = OpenAI()
    datasets_to_process = [
        "whiteOUO/Ladder-machine-learning-QA",
        "team-bay/data-science-qa",
        "mjphayes/machine_learning_questions",
        "Harikrishnan46624/AI_QA_Data",
        "Hanhhanh9/QA-AI"
    ]

    for dataset_name in datasets_to_process:
        print(f"Processing dataset: {dataset_name}")
        process_dataset(client,dataset_name)



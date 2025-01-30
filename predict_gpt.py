from openai import OpenAI
import json
from dotenv import load_dotenv
import os, csv
import asyncio
import argparse
from prompts import get_prompt


def get_model_prediction_gpt(client, question_data, prompt, model="gpt-4o"):
    try:
        # Send the question data to the OpenAI API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Question: {question_data['question']}\nChoices: {', '.join(question_data['choices'])}\n"}
            ]
        )

        # Extract and return the user's choice
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while getting the prediction for model {model}: {e}")
        return None

def get_model_prediction_o1_preview(client, question_data, prompt, model="o1-preview"):
    try:
        # 시스템 메시지 내용을 user 메시지에 포함하여 하나의 메시지로 구성합니다.
        prompt = (
            prompt + 
            f"Question: {question_data['question']}\n"
            f"Choices: {', '.join(question_data['choices'])}\n"
        )

        # o1-preview 모델은 system 역할을 지원하지 않으므로, user 메시지만 사용합니다.
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the model's answer.
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while getting the prediction for model {model}: {e}")
        return None

# 1. claude 함수 추가
# def get_model_prediction_claude



def process_and_save_responses(client, json_files, output_file, model_name, selected_prompt):
    # 2. claude 모델 이름 추가 
    # "claude" : get_model_prediction_claude
    model_dispatch = {
        "gpt-4o": get_model_prediction_gpt,
        "gpt-4": get_model_prediction_gpt,
        "gpt-3.5-turbo": get_model_prediction_gpt,
        "o1-preview": get_model_prediction_o1_preview,
    }

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Model Name", "File Name", "Question", "Choices", "Model Response", "Correct Answer"])

        for json_file in json_files:
            print(f"Processing file: {json_file}")
            with open(json_file, "r", encoding="utf-8") as file:
                questions = json.load(file)

            print(f"Using model: {model_name}")

            get_prediction = model_dispatch.get(model_name)
            if not get_prediction:
                print(f"Skipping unknown model: {model_name}")
                continue

            for question_data in questions:
                response = get_prediction(client, question_data, selected_prompt, model=model_name)
                if response is not None:
                    choices_str = "선택지:\n" + "\n".join(
                        [f"{i+1}번 - {choice}" for i, choice in enumerate(question_data["choices"])]
                    )
                    result = [
                        model_name, json_file, question_data["question"], choices_str, response, question_data["answer"]
                    ]
                    print(f"Model: {model_name}, Response: {response}, Correct Answer: {question_data['answer']}")
                    writer.writerow(result)

def main():
    """ Main function to process the experiment setup. """
    parser = argparse.ArgumentParser(description="Run OpenAI API requests with a specific model and prompt.")
    # 3. choice에 클로드 모델 추가 
    parser.add_argument("--model", type=str, required=True, choices=["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o1-preview"],
                        help="Specify the model to use.")
    parser.add_argument("--prompt", type=str, required=True, help="Specify the prompt type to use.")

    args = parser.parse_args()

    load_dotenv()
    open_api_key = os.getenv("OPENAI_API_KEY")
    # 4. api 키 추가 -> 키 두 개 불러와도 상관없겠지?
    
    # 하단 코드 너무 대충짜서 보고 조금 수정해도 돼요!
    if args.model in ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o1-preview"] :
        if open_api_key:
            client = OpenAI()  # Initialize the OpenAI client
            json_files = ["./data/data_BDA.json", "./data/data_exq.json", "./data/data_hf.json"]

            # 프롬프트 선택에 맞게 prompts.py에서 프롬프트를 불러옴
            selected_prompt = get_prompt(args.prompt)

            if selected_prompt is None:
                print(f"Error: Prompt '{args.prompt}' not found.")
                return

            # 답변 저장될 파일
            output_file = f"./responses/responses_{args.model}_{args.prompt}.csv"

            process_and_save_responses(client, json_files, output_file, args.model, selected_prompt)
            print(f"Responses saved to {output_file}")

        else:
            print("API key not found. Please set it in the .env file.")
            
    # 5. 클로드인 경우 
    # if args. model in []

if __name__ == "__main__":
    main()
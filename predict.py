from openai import OpenAI
import json
from dotenv import load_dotenv
import os, csv
import asyncio


"""def get_model_prediction(client, question_data, model="gpt-4o"):
    try:
        # Send the question data to the OpenAI API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 머신러닝 전문가입니다. 간단한 설명과 함께 선택지에서 '답:'의 형식으로 답변을 고르시오."},
                {"role": "user", "content": f"Question: {question_data['question']}\nChoices: {', '.join(question_data['choices'])}\n"}
            ]
        )

        # Extract and return the user's choice
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while getting the prediction for model {model}: {e}")
        return None"""

def get_model_prediction(client, question_data, model="o1-preview"):
    try:
        # 시스템 메시지 내용을 user 메시지에 포함하여 하나의 메시지로 구성합니다.
        prompt = (
            "당신은 머신러닝 전문가입니다. 간단한 설명과 함께 선택지에서 '답:'의 형식으로 답변을 고르시오.\n\n"
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


def process_and_save_responses(client, json_files, output_file, models):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header
        writer.writerow(["Model Name", "File Name", "Question", "Choices", "Model Response", "Correct Answer"])

        # Iterate over each JSON file
        for json_file in json_files:
            print(f"Processing file: {json_file}")

            # Load the questions from the JSON file
            with open(json_file, "r", encoding="utf-8") as file:
                questions = json.load(file)

            # Iterate over each model
            for model_name in models:
                print(f"Using model: {model_name}")

                # Iterate over each question
                for question_data in questions:
                    # Get the model's prediction
                    response = get_model_prediction(client, question_data, model=model_name)
                    if response is not None:
                        choices = question_data["choices"]
                        choices_str = "선택지:\n" + "\n".join([f"{i+1}번 - {choice}" for i, choice in enumerate(choices)])
                        result = [
                            model_name,
                            json_file,
                            question_data["question"],
                            choices_str,
                            response,
                            question_data["answer"]
                        ]
                        print(f"Model: {model_name}, Response: {response}, Correct Answer: {question_data['answer']}")
                        writer.writerow(result)


# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI()  # Initialize the OpenAI client
    json_files = ["./data/data_BDA.json", "./data/data_exq.json", "./data/data_hf.json"]  # List of JSON files
    #output_file = "responses.csv"  # Output CSV file
    #models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]  # List of model names to use

    output_file = "responses_o1-preview.csv"  # Output CSV file
    models = ["o1-preview"]  # List of model names to use

    # Run the async process
    process_and_save_responses(client, json_files, output_file, models)
    print(f"Responses saved to {output_file}")
else:
    print("API key not found. Please set it in the .env file.")

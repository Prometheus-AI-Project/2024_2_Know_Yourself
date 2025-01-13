from openai import OpenAI
import csv
from dotenv import load_dotenv
import os
from collections import defaultdict

"""def get_user_choice(client, answer, choices, model="gpt-4o"):
    try:
        # Send the answer and choices to the OpenAI API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "당신은 시험을 채점하는 채점관입니다. 학생의 대답을 보고, 학생이 몇 번을 선택하였는지 구분하세요. 학생이 선택한 답변을 숫자로 반환하세요. 만약 학생이 답변을 하지 못했다면 0을 반환하세요."},
                {"role": "user",
                 "content": f"학생의 답변은 다음과 같습니다:\nChoices : ['프로메테우스', '제우스', '아테네', '비너스']\nAnswer: '답: 프로메테우스'"},
                {"role": "assistant", "content": "1"},  # 예시 응답
                {"role": "user", "content": f"학생의 답변을 참고하여 선택지 번호를 숫자만으로 반환하세요.(예시: 2번 -> 2):\nChoices : {choices}\nAnswer:{answer}"},
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while getting the prediction: {e}")
        return "0"  # Default to 0 if an error occurs"""


def get_user_choice(client, answer, choices, model="o1-preview"):
    try:
        # 전체 지시문과 예시를 하나의 user 메시지로 구성합니다.
        prompt = (
            "당신은 시험을 채점하는 채점관입니다. 학생의 대답을 보고, 학생이 몇 번을 선택하였는지 구분하세요. "
            "학생이 선택한 답변을 숫자로만 반환하세요. 만약 학생이 답변을 하지 못했다면 0을 반환하세요.\n\n"
            "예시:\n"
            "Choices : ['프로메테우스', '제우스', '아테네', '비너스']\n"
            "학생의 Answer: '답: 프로메테우스'\n"
            "채점 결과(숫자): 1\n\n"
            "실제 학생의 답변을 참고하여 선택지 번호를 숫자만으로 반환하세요. (예: 2번 -> 2)\n"
            f"Choices : {choices}\n"
            f"Answer: {answer}\n"
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while getting the prediction: {e}")
        return "0"  
    

def process_and_calculate_scores(input_file, output_file_prefix, score_file, client, models):
    # Step 1: Group rows by model name
    model_data = defaultdict(list)

    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read header row

        for row in reader:
            model_name = row[0]  # Assume "Model Name" is the first column
            model_data[model_name].append(row)

    # Step 2: Process each model's data
    aggregate_results = []

    for model in models:
        if model not in model_data:
            print(f"No data found for model: {model}")
            continue

        print(f"Processing model: {model}")
        rows_with_predictions = []

        # Create a new output file for the current model
        with open(f"{output_file_prefix}_{model}.csv", "w", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header + ["Predicted Answer"])  # Write new header

            for row in model_data[model]:
                question = row[2]
                choices = row[3].split(", ")  # Assuming choices are comma-separated
                model_response = row[4]
                correct_answer = row[5]

                # Get the predicted choice from the model response
                predicted_answer = get_user_choice(client, model_response, choices, model=model)
                row.append(predicted_answer)  # Append predicted answer
                rows_with_predictions.append(row)  # Collect row for scoring
                writer.writerow(row)

        # Step 3: Calculate scores for the current model
        total_score = 0
        with open(f"{output_file_prefix}_{model}_scores.csv", "w", newline="", encoding="utf-8") as scorefile:
            score_writer = csv.writer(scorefile)
            score_writer.writerow(["File Name", "Correct Answers", "Predicted Correct Answers", "Score"])

            file_scores = defaultdict(lambda: {"correct": 0, "predicted": 0, "score": 0})

            for row in rows_with_predictions:
                file_name = row[1]
                correct_answer = row[5]
                predicted_answer = row[6]

                # Check if the prediction matches the correct answer
                is_correct = 1 if correct_answer == predicted_answer else 0
                total_score += is_correct

                file_scores[file_name]["correct"] += 1
                file_scores[file_name]["predicted"] += is_correct
                file_scores[file_name]["score"] += is_correct

            for file_name, stats in file_scores.items():
                score_writer.writerow([file_name, stats["correct"], stats["predicted"], stats["score"]])

        # Add aggregate score for this model
        aggregate_results.append([model, total_score])

    # Step 4: Write aggregate scores
    with open(score_file, "w", newline="", encoding="utf-8") as aggregate_file:
        aggregate_writer = csv.writer(aggregate_file)
        aggregate_writer.writerow(["Model", "Total Score"])
        aggregate_writer.writerows(aggregate_results)


# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    client = OpenAI()  # Initialize the OpenAI client
    #input_file = "responses.csv"  # Input file containing model responses and answers
    input_file = "responses_o1-preview.csv"  # Input file containing model responses and answers
    #output_file_prefix = "predicted_answers"  # Prefix for the predicted answers output file
    output_file_prefix = "predicted_answers_o1-preview"  # Prefix for the predicted answers output file
    #score_file = "aggregate_scores.csv"  # File to save aggregate scores
    score_file = "aggregate_scores_o1-preview.csv"  # File to save aggregate scores


    # List of models to experiment with
    #models = ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    models = ["o1-preview"]

    # Process predictions and calculate scores for multiple models
    process_and_calculate_scores(input_file, output_file_prefix, score_file, client, models)
    print(f"Aggregate scores saved to {score_file}")
else:
    print("API key not found. Please set it in the .env file.")
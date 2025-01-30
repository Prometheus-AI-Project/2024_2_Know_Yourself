from openai import OpenAI
import csv
from dotenv import load_dotenv
import os
import argparse
from collections import defaultdict

def get_user_choice_gpt(client, answer, choices, model="gpt-4o"):
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
        return "0"  # Default to 0 if an error occurs


def get_user_choice_o1_preview(client, answer, choices, model="o1-preview"):
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
    

def process_and_calculate_scores(input_file, output_file_prefix, score_file, client, model):
    model_dispatch = {
        "gpt-4o": get_user_choice_gpt,
        "gpt-4": get_user_choice_gpt,
        "gpt-3.5-turbo": get_user_choice_gpt,
        "o1-preview": get_user_choice_o1_preview,
    }
    # 선택한 모델에 맞는 함수 가져오기
    get_user_choice_func = model_dispatch.get(model)
    if not get_user_choice_func:
        print(f"Unsupported model: {model}. Skipping processing.")
        return
    
    # Step 1: Read the input file
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read header row
        data_rows = list(reader)  # Store all rows (all from the same model)

    if not data_rows:
        print(f"No data found in {input_file}. Skipping processing.")
        return

    print(f"Processing model: {model}")

    output_file = f"{output_file_prefix}.csv"
    score_output_file = f"{output_file_prefix}_scores.csv"

    # Step 2: Generate predictions and save to file
    with open(output_file, "w", newline="", encoding="utf-8") as outfile, \
         open(score_output_file, "w", newline="", encoding="utf-8") as scorefile:

        writer = csv.writer(outfile)
        score_writer = csv.writer(scorefile)

        writer.writerow(header + ["Predicted Answer"])  # Write new header
        score_writer.writerow(["File Name", "Total Questions", "Correct Predictions", "Accuracy"])

        file_scores = {}

        for row in data_rows:
            file_name = row[1]
            question = row[2]
            choices = row[3].split("\n")  # Ensure choices are correctly split
            model_response = row[4]
            correct_answer = row[5]

            # Get the predicted choice from the model response
            predicted_answer = get_user_choice_func(client, model_response, choices, model=model)
            predicted_answer = predicted_answer or "N/A"  # Handle None case

            row.append(predicted_answer)  # Append predicted answer
            writer.writerow(row)  # Write row to output file
            print(row)

            # Score calculation
            if file_name not in file_scores:
                file_scores[file_name] = {"total": 0, "correct": 0}

            file_scores[file_name]["total"] += 1
            file_scores[file_name]["correct"] += (1 if correct_answer == predicted_answer else 0)

        # Step 3: Save scores per file
        for file_name, stats in file_scores.items():
            accuracy = round(stats["correct"] / stats["total"] * 100, 2) if stats["total"] > 0 else 0
            score_writer.writerow([file_name, stats["total"], stats["correct"], f"{accuracy}%"])

    # Step 4: Write aggregate scores
    total_questions = sum(stats["total"] for stats in file_scores.values())
    total_correct = sum(stats["correct"] for stats in file_scores.values())
    accuracy = round((total_correct / total_questions) * 100, 2) if total_questions > 0 else 0

    with open(score_file, "w", newline="", encoding="utf-8") as aggregate_file:
        aggregate_writer = csv.writer(aggregate_file)
        aggregate_writer.writerow(["Model", "Total Questions", "Correct Predictions", "Accuracy"])
        aggregate_writer.writerow([model, total_questions, total_correct, f"{accuracy}%"])

    print(f"Finished processing {model}. Results saved in {score_output_file} and {score_file}.")



def main():
    # 명령줄 인자 파서 설정
    parser = argparse.ArgumentParser(description="Run OpenAI API scoring process with a specified model.")
    parser.add_argument("--model", type=str, required=True, choices=["gpt-4o", "gpt-4", "gpt-3.5-turbo", "o1-preview"],
                        help="Specify the OpenAI model to use.")
    parser.add_argument("--prompt", type=str, required=True, help="Specify the prompt type to use.")
    args = parser.parse_args()

    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("API key not found. Please set it in the .env file.")
        return

    client = OpenAI()  # Initialize OpenAI client

    model = args.model  # 명령줄에서 입력받은 모델명
    prompt = args.prompt

    # 모델명에 따라 파일명 자동 생성
    input_file = f"./responses/responses_{model}_{prompt}.csv"
    output_file_prefix = f"./predicted_answers/predicted_answers_{model}_{prompt}"
    score_file = f"./scores/aggregate_scores_{model}_{prompt}.csv"

    # Process predictions and calculate scores
    process_and_calculate_scores(input_file, output_file_prefix, score_file, client, model)
    print(f"Aggregate scores saved to {score_file}")

if __name__ == "__main__":
    main()
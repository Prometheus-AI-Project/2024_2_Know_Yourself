# Know_Yourself(~ing)
## 🔥 인공지능 지식 LLM 리더보드(~ing 임시)

(사진 첨부)

## 🤖 인공지능 지식 LLM 리더보드란?

인공지능 지식 LLM 리더보드는 인공지능에 관련된 기출문제들을 기반으로 한 벤치마크 리더보드입니다.


+보충

## 💯 리더보드 순위
(모델 추가 예정)
| Leaderboard Rank |          Model Name          | Submitter Name | Total Score | Hugging Face(49) | 기출문제(40) | 빅데이터 분석기사(일부)(40) |
|:----------------:|:----------------------------:|:--------------:|:-----------:|:------------:|:--------:|:----------------------:|
|         1st        |       gpt-4o	            |      OpenAI     |     102    |      30      |     35   |          36            |
|         2nd        |       o1-preview	             |      OpenAI       |     91    |      23      |     34   |          34            |
|         2nd        |       gpt-4	             |      OpenAI       |     91    |      20      |     35   |          36            |
|         3rd        |       gpt-3.5-turbo            |      OpenAI     |     65    |      15      |     27   |          23            |
                    

## 📚 Benchmark 데이터셋
- [Hugging Face brucewlee1/mmlu-machine-learning 일부 번역](https://huggingface.co/datasets/brucewlee1/mmlu-machine-learning)
- 국가공무원 7급 공채 제2차 필기시험(인공지능) 기출문제
- ADSP 기출문제
- 빅데이터분석기사 기출문제



## ✏ 평가
### predict.py
- 각 질문에 대한 답변 생성
- 프롬프트
```
messages=
    [
        {"role": "system", "content": "당신은 머신러닝 전문가입니다. 간단한 설명과 함께 선택지에서 '답:'의 형식으로 답변을 고르시오."},
        {"role": "user", "content": f"Question: {question_data['question']}\nChoices: {', '.join(question_data['choices'])}\n"}
    ]
```

### score.py
- 나온 답변에서 LLM이 정답을 추출
- 추출한 정답과 답안지를 비교하여 최종점수 산정
- 프롬프트(one-shot)
```
messages=[
                {"role": "system",
                 "content": "당신은 시험을 채점하는 채점관입니다. 학생의 대답을 보고, 학생이 몇 번을 선택하였는지 구분하세요. 학생이 선택한 답변을 숫자로 반환하세요. 만약 학생이 답변을 하지 못했다면 0을 반환하세요."},
                {"role": "user",
                 "content": f"학생의 답변은 다음과 같습니다:\nChoices : ['프로메테우스', '제우스', '아테네', '비너스']\nAnswer: '답: 프로메테우스'"},
                {"role": "assistant", "content": "1"},  # 예시 응답
                {"role": "user", "content": f"학생의 답변을 참고하여 선택지 번호를 숫자만으로 반환하세요.(예시: 2번 -> 2):\nChoices : {choices}\nAnswer:{answer}"},
            ]
```

🤔2단계로 나눈 이유
LLM이 답변을 생성할 때 일관성을 유지하기 위하여 2단계로 나누었습니다.예를 들어 '숫자만으로 답하시오' 라고 명령했음에도 불구하고, '2번', '2번이 정답입니다.', '프로메테우스' 등과 같이 다양한 형식으로 답변을 생성하는 문제가 발생하였는데 이는 모두 오답으로 처리되어 평가 결과 신뢰성이 떨어질 수 있습니다. 이를 해결하기 위해 2단계로 나누어 평가 프로세스를 개선하였습니다.


## 👥 멤버
| 심수민       | 김예지                        | 이연우                          |
|:----------:|:------------------------------:|:------------------------------------:|
| ![Alice 사진](https://via.placeholder.com/100)      | ![Alice 사진](https://via.placeholder.com/100) | ![Alice 사진](https://via.placeholder.com/100) |
| [use08174](https://github.com/use08174)        |  [jyhannakim](https://github.com/jyhannakim)  |  [yeonu2](https://github.com/yeonu2)    |

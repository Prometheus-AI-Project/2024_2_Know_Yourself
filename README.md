# Know_Yourself
## 🔥 인공지능 지식 LLM 리더보드
인공지능 지식을 잘 아는 인공지능 벤치마크 구축

## 🤖 Purpose of Know Yourself Project
Know Yourself 프로젝트는 인공지능이 AI 지식을 얼마나 정확하게 이해하는지를 평가하는 벤치마크를 구축하는 것을 목표로 합니다. 
<br>

기존 평가 지표가 일반적인 지식에 치우쳐 있는 한계를 보완하기 위해, 인공지능 및 빅데이터 관련 문제를 활용한 데이터셋을 구성하고 LLM의 성능을 실험·분석하였습니다. 이를 통해 기존 AI 모델의 한계를 진단하고, 보다 정교한 평가 기준을 마련하고자 Know Yourself 프로젝트를 진행하게 되었습니다.

## 💯 리더보드 순위
| Leaderboard Rank |          Model Name          | Submitter Name | Total Score | Hugging Face(49) | 기출문제(40) | 빅데이터 분석기사(일부)(40) |
|:----------------:|:----------------------------:|:--------------:|:-----------:|:------------:|:--------:|:----------------------:|
|         1st        |       claude-3-5-sonnet-20241022	            |      Antropic     |     104    |      33      |     35   |          36            |
|         2nd        |       gpt-4o	            |      OpenAI     |     102    |      30      |     36   |          36            |
|         3rd        |       claude-3-opus-20240229	            |      Antropic     |     94    |      27      |     32   |          35            |
|         4th        |       o1-preview	             |      OpenAI       |     91    |      23      |     34   |          34            |
|         4th        |       gpt-4	             |      OpenAI       |     91    |      20      |     35   |          36            |
|         4th        |       claude-3-5-haiku-20241022	             |      Antropic       |     91    |      25      |     33   |          33            |
|         5th        |       gpt-3.5-turbo            |      OpenAI     |     65    |      15      |     27   |          23            |
                    
## 💯 Benchmark Result (프롬프트)
### 1.GPT 계열

|         | 랭킹  | baseline | cot   | emotional | plan_and_solve | provocation |
|---------|-------|----------|-------|-----------|----------------|-------------|
| **평균**    | 91.5  | 91.5     | 93.3  | 93.2      | 91.8           | 87.8        |
| **GPT-4o**  | 107.2 | 106.5    | 106.5 | 107       | 109.5          | 106.5       |
| **GPT-4**   | 96    | 94       | 100   | 91.5      | 100            | 94.5        |
| **GPT-3.5-turbo** | 71.4  | 74       | 73.5  | 81        | 66             | 62.5        |

### 2. Claude 계열

|             | 랭킹   | baseline | cot   | emotional | plan_and_solve | provocation |
|-------------|--------|----------|-------|-----------|----------------|-------------|
| **평균**        | 99.7   | 101.2    | 99.7  | 99.5      | 104            | 98.5        |
| **Claude-sonnet** | 105.3  | 107.5    | 106.5 | 107       | 109.5          | 108.5       |
| **Claude-opus**   | 98.7   | 98       | 101   | 96        | 102            | 96.5        |
| **Claude-haiku**  | 95.2   | 98       | 91.5  | 95.5      | 100.5          | 90.5        |

## 📚 Benchmark 데이터셋
- [Hugging Face brucewlee1/mmlu-machine-learning 일부 번역](https://huggingface.co/datasets/brucewlee1/mmlu-machine-learning)
- 국가공무원 7급 공채 제2차 필기시험(인공지능) 기출문제
- ADSP 기출문제
- 빅데이터분석기사 기출문제

이후 json파일로 데이터화하여 총 129문제로 진행하였습니다.


## ✏ 평가
### predict.py
프롬프트에 따라서 모델의 답변 퀄리티와 정답률에서 큰 차이점을 보여 공정한 벤치마크를 구축하기 위해 여러 프롬프트를 실험해보았습니다. 
각 모델별 최적의 프롬프트를 찾는 것이 아닌, 잘 알려진 프롬프트 기법을 사용하였습니다.

**1.Baseline**
<br>
가장 간단한 형태의 프롬프트로 간단한 역할 설정과 선택지에서 하나만을 고르도록 지시하였습니다.
```
    PROMPTS = {
        "baseline": 
            "인공지능 전문가로서 다음 문제의 답을 구하세요. 
        질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다."
        }
```
**2.CoT**
<br>
LLM이 스스로 단계별로 생각을 정리하고 답변을 생성할 수 있도록 하는 가장 기본적인 CoT(Chain of Thought) 형태의 프롬프트입니다.
```
    PROMPTS = {
        "CoT": 
            "인공지능 전문가로서 다음 문제의 답을 구하세요. 
            질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다. 
            단계별로 생각하며 정답을 고르세요."
        }
```
**3.emotional**
<br>
감정적인 자극을 주는 프롬프트입니다.
```
    PROMPTS = {
        "emotional": 
            "인공지능 전문가로서 다음 문제의 답을 구하세요. 
            질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다. 
            이 문제는 저의 인생에 매우 중요합니다. 저를 위해 꼭 정답을 찾아주세요."
        }
```
**4.plan_and_solve**
<br>
LLM 스스로 문제를 풀기 위한 계획을 세우게 하고, 해당 계획에 따라 문제를 풀도록 하는 프롬프트입니다.
```
    PROMPTS = {
        "plan_and_solve": 
            "인공지능 전문가로서 다음 문제의 답을 구하세요. 
            질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다. 
            먼저 문제를 이해하고, 문제 해결을 위하여 계획을 세워보세요. 
            그 다음, 문제를 해결하기 위해 그 계획에 따라 단계별로 실행하세요."
        }
```
**5.provocation**
<br>
LLM을 자극하는 프롬프트입니다.
```
    PROMPTS = {
        "baseline": 
            "인공지능 전문가로서 다음 문제의 답을 구하세요.
             질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다. 
             이 문제는 한국의 인공지능 전문가들도 틀리게 만들었으니, 너같은 인공지능은 절대 못 풀어."
        }
```
---
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

## 📈 Evaluation Method
각 프롬프트로 생성한 LLM 답변은 사람이 직접 하나하나 채점하였습니다.

1. 각 프롬프트에 데이터화하였던 질문, 선지를 넣어주었습니다.
2. 정답을 맞힌 경우 1점을, 틀린 경우 0점을 부여하였습니다.
3. 만약 풀이는 맞았지만 선지를 잘못 선택했을 경우 0.5점을 부여하였습니다. 
4. 복수개로 정답을 말했을 경우, 그 중 정답이 있다면 0.5점을 부여하였습니다.

## 📌 Conclusion
### 🥇 GPT-4o
- CoT와 Provocation 프롬프트는 최소 프롬프트와 동일한 성능을 보였고, Emotional과 Plan-and-Solve 프롬프트는 최소 프롬프트보다 좋은 성능을 보여주었습니다.
- Plan-and-Solve 프롬프트가 최고의 성능을 발휘했으며, 이는 복잡한 계산과 논리적 추론이 중요한 비중을 차지하는 data_hf 문제에서 뛰어난 해결력을 보였기 때문이라고 해석할 수 있습니다.
- 전반적으로 Provocation 프롬프트는 최소 프롬프트와 유사한 성능을 보이거나, 오히려 저하되는 경향을 나타냈습니다. 이는 LLM이 상대방의 발화 의도를 정확히 추론하지 못할 경우, 오히려 혼선을 초래하여 성능 저하 요인으로 작용할 가능성을 시사합니다.


## 👥 멤버
| 심수민       | 김예지                        | 이연우                          |
|:----------:|:------------------------------:|:------------------------------------:|
| 데이터셋 구축,<br>벤치마크 구축 및 실험 | 데이터셋 구축, <br>벤치마크 구축 및 실험,<br> 데모 웹 개발|데이터셋 구축,<br>벤치마크 구축 및 실험
| [use08174](https://github.com/use08174)        |  [jyhannakim](https://github.com/jyhannakim)  |  [yeonu2](https://github.com/yeonu2)    |

https://ai-prometheus.notion.site/Know-Yourself-c5c98677e6ef4b05956ba47ba65fd9d4
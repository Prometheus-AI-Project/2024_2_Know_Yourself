<template>
      <div class="image-container">
        <img src="/assets/quiz.png" alt="Description of image">
        </div>
    <div class="test-container">
      <div class="progress-container">
        <div class="progress-info">
          {{ currentQuestionIndex + 1 }}/{{ totalQuestions }}
        </div>
        <!-- 진행도 막대 -->
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
      </div>
  
      <!-- 실제 문제 -->
      <h2 class="question-text">
        {{ currentQuestion.question }}
      </h2>
  
      <!-- 4지 선다 선택지 -->
      <div class="options-wrapper">
        <div
          v-for="(option, i) in currentQuestion.options"
          :key="i"
          class="option"
          :class="{ selected: userAnswers[currentQuestionIndex] === i }"
          @click="selectOption(i)"
        >
          {{ option }}
        </div>
      </div>
  
      <!-- 다음 문제 또는 제출하기 버튼 -->
      <div class="button-container">
        <button
          v-if="currentQuestionIndex < totalQuestions - 1"
          @click="goNext"
        >
          다음 문제
        </button>
        <button
          v-else
          @click="submitQuiz"
        >
          제출하기
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TestPage',
    data() {
      return {
        questions: [
          {
            question: "딥러닝에 대한 설명으로 옳은 것은?",
            options: [
              "오차역전파를 사용한다.",
              "ReLU보다 Sigmoid를 사용한다.",
              "딥러닝은 각 은닉층의 가중치를 통해 모형의 결과를 해석하기 용이하다.",
              "Dropout은 무작위 비율로 신경망을 제거한다."
            ], 
            correctIndex: 0,
            explanationGPT: "해결 계획: 제시된 선택지를 하나씩 살펴보며 딥러닝에 대한 올바른 설명인지 확인한다. <br> 1. 오차역전파를 사용한다: 딥러닝에서는 각 계층의 가중치를 업데이트하는 방법으로 오차역전파를 사용합니다. 따라서 이 설명은 옳습니다. <br><br>2. ReLU보다 Sigmoid를 사용한다: 이는 확실하게 말할 수 없는 점입니다. ReLU와 Sigmoid는 둘 다 활성화 함수로써 널리 사용되지만, 각각의 장단점이 있습니다. 일반적으로 ReLU는 Sigmoid보다 빠른 수렴 속도와 기울기 소실 문제 해결 등의 이점 때문에 선호되는 경향이 있습니다.<br><br> 3. 딥러닝은 각 은닉층의 가중치를 통해 모형의 결과를 해석하기 용이하다: 이는 옳지 않습니다. 딥러닝의 큰 단점 중 하나는 각 은닉층의 가중치를 통해 모델의 결과를 명확하게 이해하기 어렵다는 것입니다. 이를 '블랙박스' 문제라고 부릅니다.<br><br> 4. Dropout은 무작위 비율로 신경망을 제거한다: Dropout은 일반적으로 신경망의 특정 레이어에서 무작위로 뉴런들을 제거(가중치를 0으로 설정)하는 것을 의미합니다. 이 방법은 일종의 규제 방법으로 모델이 과적합되는 것을 방지하는 데 도움을 줍니다. <br><br>따라서, 이 문제의 올바른 답변은 오차역전파를 사용한다인 1번입니다.",
            explanationClaude: `이 문제를 해결하기 위한 계획을 세워보겠습니다: <br><br> 1. 각 선택지의 내용을 딥러닝의 핵심 특징과 비교 검토
2. 각 선택지의 정확성 평가 <br><br>
3. 가장 정확한 설명 선택<br><br>

각 선택지 분석:<br>

1. "오차역전파를 사용한다"
- 맞음: 딥러닝은 오차역전파(backpropagation)를 사용하여 가중치를 업데이트
<br>
2. "ReLU보다 Sigmoid를 사용한다"
- 틀림: 현대 딥러닝에서는 주로 ReLU를 더 선호 (기울기 소실 문제 해결, 계산 효율성)
<br>
3. "딥러닝은 각 은닉층의 가중치를 통해 모형의 결과를 해석하기 용이하다"
- 틀림: 딥러닝은 블랙박스 모델로 해석이 매우 어려움
<br>
4. "Dropout은 무작위 비율로 신경망을 제거한다"
- 맞음: Dropout은 학습 과정에서 무작위로 뉴런을 비활성화
<br>
결론:
선택지 1번이 가장 정확합니다. 오차역전파는 딥러닝의 핵심적인 학습 알고리즘으로, 모든 딥러닝 모델에서 기본적으로 사용되는 방법입니다.
<br><br>
답: 1`
          },
          {
            question: "다음 중 자연어 처리(NLP) 기법으로 가장 적합하지 않은 것은?",
            options: [
              "ELMo",
              "GPT",
              "BERT",   
              "YOLO"
            ],
            correctIndex: 3,
            explanationGPT: "자연어 처리(NLP, Natural Language Processing)는 인간의 언어를 컴퓨터가 이해하고 분석하는 것을 목표로 하는 인공지능의 한 분야입니다. 이 질문에서 주어진 선택지 중에 ELMo, GPT, BERT는 모두 NLP에 쓰이는 모델들입니다. 1) ELMo(Embeddings from Language Models)는 자연어 처리를 위한 딥러닝 모델 중 하나로, 문맥에 따른 단어의 의미를 잘 표현할 수 있도록 설계되었습니다. 2) GPT(Generative Pre-Training) 역시 자연어 처리를 위한 transformer 기반의 모델로, 텍스트 생성 등의 다양한 NLP 태스크에 사용됩니다. 3) BERT(Bidirectional Encoder Representations from Transformers)는 특히 문맥을 양방향으로 파악하는 데 강점을 가진 모델입니다. BERT는 높은 성능으로 많은 NLP 태스크에서 사용됩니다. 그러나 선택지에 있는 4) YOLO(You Only Look Once)는 자연어 처리에 쓰이는 모델이 아닙니다. YOLO는 실시간 객체 탐지(object detection) 알고리즘으로, 이미지를 한번만 보고 객체를 탐지하는 데 사용됩니다. 자연어 처리와는 별개의 영역인 컴퓨터 비전 분야에서 주로 활용됩니다. 정답은 '4. YOLO'입니다.",
            explanationClaude: `이 문제를 해결하기 위한 계획을 세워보겠습니다:<br><br>

1. 각 선택지의 기술이 무엇인지 파악하기
2. 각 기술이 자연어 처리와 관련이 있는지 확인하기
3. 가장 적합하지 않은 것 선택하기
<br><br>
단계별 분석:
<br>
1. 각 기술 설명:
- ELMo: Embeddings from Language Models, 문맥을 고려한 단어 임베딩 모델
- GPT: Generative Pre-trained Transformer, 자연어 생성을 위한 언어 모델
- BERT: Bidirectional Encoder Representations from Transformers, 양방향 언어 모델
- YOLO: You Only Look Once, 실시간 객체 탐지를 위한 컴퓨터 비전 알고리즘
<br><br>
2. 자연어 처리 관련성:
- ELMo: 자연어 처리를 위한 단어 임베딩 모델 (O)
- GPT: 자연어 처리와 생성을 위한 언어 모델 (O)
- BERT: 자연어 이해를 위한 언어 모델 (O)
- YOLO: 이미지 처리와 객체 탐지를 위한 모델 (X)
<br><br>
3. 결론:
YOLO는 컴퓨터 비전 분야의 기술로, 자연어 처리와는 관련이 없습니다.
<br><br>
따라서, 답은 4번 YOLO입니다.`
          },
          {
            question: "K-means 군집분석의 설명에 대해 옳은 것은?",
            options: [
              "초기 중심점 선택에 따라 결과가 달라질 수 있다.",
              "이상치에 민감하지 않다.",
              "범주형 변수에 대해 직접 적용이 가능하다.",
              "군집의 개수 K를 사전에 지정할 필요가 없다."
            ],
            correctIndex: 0,
            explanationGPT: "먼저, 이 문제는 K-means 군집분석에 대한 이해를 테스트하는 것임을 알 수 있습니다. K-means 군집분석에 대한 기본적인 지식을 토대로 이해하고 답을 찾아보겠습니다. <br><br>1. 계획 세우기: - 각 선택지가 K-means 군집분석의 주된 특성과 일치하는지 파악함으로써, 옳은 선택지를 찾을 수 있습니다. <br> 2. 계획 실행하기: <br><br> - 선택지 1: '초기 중심점 선택에 따라 결과가 달라질 수 있다'는 명언으로 K-means 알고리즘 특성 중 하나입니다. 따라서 이 선택지는 옳습니다. <br><br> - 선택지 2: '이상치에 민감하지 않다'는 K-means의 특성을 정확하게 반영하지 않습니다. 실제로 K-means 알고리즘은 이상치에 매우 민감합니다. <br><br>- 선택지 3: '범주형 변수에 대해 직접 적용이 가능하다'는 또한 부정확합니다. K-means 알고리즘은 유클리디안 거리를 사용하여 클러스터 중심을 계산하므로 연속형 변수에 적합합니다. <br><br>- 선택지 4: '군집의 개수 K를 사전에 지정할 필요가 없다'는 잘못된 정보입니다. K-means 알고리즘의 이름에서 알 수 있듯이, 우리는 사전에 군집의 개수 K를 지정해야 합니다. <br><br>- 검토 단계: - 위 단계를 통해 K-means 군집분석에 가장 잘 부합하는 올바른 선택지는 '초기 중심점 선택에 따라 결과가 달라질 수 있다'입니다. 따라서, 문제의 답은 1번입니다.",
            explanationClaude: `이 문제를 해결하기 위한 계획을 세워보겠습니다.<br><br>

1. K-means 군집분석의 주요 특징들을 검토
2. 각 선택지의 내용을 K-means의 특성과 비교 분석
3. 정확한 답 선택
<br><br>
분석과정:

1. K-means 군집분석의 주요 특징:
- K값(군집 수)을 사전에 지정해야 함
- 수치형 데이터에 적용
- 초기 중심점 선택이 결과에 영향을 미침
- 이상치에 민감함
<br><br>
2. 각 선택지 분석:
1번: "초기 중심점 선택에 따라 결과가 달라질 수 있다"
- 맞음. K-means는 초기 중심점 선택에 따라 다른 결과가 나올 수 있음
<br><br>
2번: "이상치에 민감하지 않다"
- 틀림. K-means는 이상치에 매우 민감함
<br><br>
3번: "범주형 변수에 대해 직접 적용이 가능하다"
- 틀림. K-means는 수치형 데이터에만 직접 적용 가능
<br><br>
4번: "군집의 개수 K를 사전에 지정할 필요가 없다"
- 틀림. K-means는 반드시 K값을 사전에 지정해야 함
<br><br>
따라서, 정답은 1번 "초기 중심점 선택에 따라 결과가 달라질 수 있다" 입니다.`
          },
          {
            question: "합성곱 신경망(CNN, Convolutional Neural Network)에 대한 설명으로 옳지 않은 것은?",
            options: [
              "이미지 분류 업무에 CNN을 활용할 수 있다.",
              "CNN 내부에는 여러 개의 합성곱(convolution)층과 풀링(pooling)층을 배치할 수 있다.",
              "CNN에서는 완전 연결(fully connected)층이 사용되지 않는다.",
              " CNN에서는 학습 데이터에 과적합(overfitting)되는 문제를 해결하기 위해 드롭아웃(dropout) 기법이 사용될 수 있다."
            ],
            correctIndex: 2,
            explanationGPT: "아래와 같이 문제를 해결해보겠습니다. <br><br>1. 문제 이해: 이 질문은 합성곱 신경망(CNN)에 대한 개념을 검증하고 있습니다. 네 개의 선택지 가운데 하나가 오답이며, 이를 찾아야 합니다. <br><br>2. 계획 세우기: CNN에 대한 이해와 기초 지식을 토대로 각 선택지를 검토하겠습니다.  <br><br>3. 단계별로 실행하기: <br><br>- 선택지 1: 이미지 분류 업무에 CNN을 활용할 수 있다. (정답) <br><br>- 선택지 2: CNN 내부에는 여러 개의 합성곱(convolution)층과 풀링(pooling)층을 배치할 수 있다. (정답) <br><br>- 선택지 3: CNN에서는 완전 연결(fully connected)층이 사용되지 않는다. (오답) <br><br>- 선택지 4: CNN에서는 학습 데이터에 과적합(overfitting)되는 문제를 해결하기 위해 드롭아웃(dropout) 기법이 사용될 수 있다. (정답) 들어, 선택지 3이 합성곱 신경망(CNN)에 대한 올바르지 않은 설명입니다. CNN 구조는 일반적으로 여러 개의 합성곱 계층과 풀링 계층 이후에 완전 연결계층이 사용됩니다. 이렇게 하면 공간적인 특징을 캡처한 후 이 정보를 기반으로 분류 작업을 수행할 수 있습니다. 따라서 완전 연결층은 CNN에서 중요한 부분을 담당합니다.  따라서 정답은 3번입니다.",
            explanationClaude: `이 문제를 해결하기 위한 계획을 세워보겠습니다.
<br><br>
1. CNN의 주요 특징들을 나열해봅니다.
2. 각 선택지의 내용이 CNN의 특징과 일치하는지 검토합니다.
3. 잘못된 설명을 찾아냅니다.
<br><br>
각 선택지를 검토해보겠습니다:
<br><br>
1. "이미지 분류 업무에 CNN을 활용할 수 있다."
- 맞습니다. CNN은 이미지 처리와 분류에 매우 효과적이며, 실제로 가장 많이 활용되는 분야입니다.
<br><br>
2. "CNN 내부에는 여러 개의 합성곱층과 풀링층을 배치할 수 있다."
- 맞습니다. CNN의 기본 구조는 여러 개의 합성곱층과 풀링층으로 구성됩니다.
<br><br>
3. "CNN에서는 완전 연결층이 사용되지 않는다."
- 틀렸습니다. CNN은 일반적으로 마지막 부분에 완전 연결층을 포함합니다. 합성곱층과 풀링층을 통해 추출된 특징들을 최종적으로 분류하기 위해 완전 연결층이 사용됩니다.
<br><br>
4. "CNN에서는 학습 데이터에 과적합되는 문제를 해결하기 위해 드롭아웃 기법이 사용될 수 있다."
- 맞습니다. 드롭아웃은 CNN을 포함한 대부분의 신경`
          },
          {
            question: "컴퓨터 비전 관련 딥러닝 모델에 대한 설명으로 옳지 않은 것은?",
            options: [
              "YOLO는 정확도보다 처리 속도에 강점을 갖는 객체 탐지 및 분류 모델이다.",
              "R-CNN 모델에서는 객체 탐지와 분류를 동시에 수행하므로 효율성이 높다.",
              "Fast R-CNN 모델에서는 입력 영상에서 객체를 탐지하기 위해 선택적 탐색 알고리즘을 사용한다.",
              "SSD(Single Shot Detector)는 YOLO에 비해 객체 탐지 및 분류의 정확도와 처리 속도가 개선된 모델이다."
            ],
            correctIndex: 1,
          explanationGPT: `먼저, 문제 추론에 앞서 각 모델의 특징을 이해해야 합니다.  <br><br>YOLO(You Only Look Once)는 객체 탐지 모델로, 매우 높은 처리 속도를 가지며 실시간 환경에서 객체 탐지에 적합합니다.
  R-CNN(Regions with CNN)의 경우, 수많은 제안 영역(proposal areas)을 생성하고 각각에 대해 CNN을 실행하여 객체를 인식하고 분류합니다. 이는 효율적인 방법은 아닙니다.
  Fast R-CNN은 R-CNN의 단점을 개선한 모델로, 이미지를 한 번에 통과시키고 특성 맵을 사용해서 각 제안 영역에서 객체를 인식합니다. 이는 R-CNN보다 빠르지만, 여전히 제안 영역(proposal areas)을 생성하기 위한 선택적 탐색(selective search) 알고리즘으로 인해 속도가 느려집니다.SSD(Single Shot Detector)는 'YOLO비교 객체 탐지 및 분류의 정확도와 처리 속도'가 모두 개선된 모델이 아닐 가능성이 높다. YOLO와 SSD는 비슷한 방법을 사용하여 객체 탐지를 수행하며, 둘 사이의 성능은 사용되는 데이터셋과 설정에 따라 다르지만, 일반적으로 높은 정확도와 실시간 처리 속도를 얻기 어렵습니다.
<br><br>
  따라서 계획은 이러한 세부 정보를 바탕으로 선택지를 개별적으로 평가하는 것입니다.
<br><br>
  번역: YOLO는 정확도보다 처리 속도에 강점을 갖는 객체 탐지 및 분류 모델이다 (이것은 사실입니다)
  R-CNN 모델에서는 객체 탐지와 분류를 동시에 수행하므로 효율성이 높다 (이것은 틀렸습니다. R-CNN은 이런 방식으로 동작하지만 효율성이 높다고 말하기는 어렵습니다)
  Fast R-CNN 모델에서는 입력 영상에서 객체를 탐지하기 위해 선택적 탐색 알고리즘을 사용한다(사실입니다. Fast R-CNN은 선별적 탐색을 사용합니다)
  SSD(Single Shot Detector)는 YOLO에 비해 객체 탐지 및 분류의 정확도와 처리 속도가 개선된 모델이다(이것은 전적으로 사실이 아닙니다. 두 모델의 성능은 다양한 요인에 따라 달라집니다)
  결국, 선택지 중에서 'R-CNN 모델에서는 객체 탐지와 분류를 동시에 수행하므로 효율성이 높다'가 틀린 설명입니다. 따라서 답은 2번입니다.`,
            explanationClaude: `이 문제를 해결하기 위한 계획:<br><br>
1. 각 보기에 언급된 컴퓨터 비전 모델들의 특징을 검토
2. 각 모델의 주요 특성과 작동 방식을 비교
3. 잘못된 설명을 찾아내기
<br><br>
각 보기 분석:
1. YOLO: 맞음
- 실시간 처리가 가능한 빠른 속도가 장점
- 정확도는 다른 모델들에 비해 상대적으로 낮음
<br><br>
2. R-CNN: 틀림
- R-CNN은 객체 탐지와 분류를 순차적으로 수행
- 선택적 탐색으로 관심 영역 추출 후 CNN으로 특징 추출
- 이후 SVM으로 분류를 수행
- 이러한 순차적 과정으로 인해 처리 시간이 길고 효율성이 낮음
<br><br>
3. Fast R-CNN: 맞음
- 선택적 탐색(Selective Search) 알고리즘 사용
- 관심 영역을 찾아내는데 사용
<br><br>
4. SSD: 맞음
- YOLO보다 개선된 정확도와 속도를 보임
- 다양한 크기의 특징 맵을 사용하여 성능 향상
<br><br>
따라서 답은 2번입니다. R-CNN이 객체 탐지와 분류를 동시에 수행한다는 설명은 잘못되었습니다. R-CNN은 순차적 처리로 인해 효율성이 낮은 것이 특징입니다.`
          },
          {
            question: "인공신경망에 대한 설명으로 가장 알맞지 않은 것은?",
            options: [
              "인공신경망에서 역전파는 입력층(Input Layer)에서 출력층(Output Layer)까지 정보가 전달되는 과정이다.",
              "인공신경망은 입력값을 받아서 출력값을 만들기 위해 촬성화 함수를 사용한다.",
              "인공신경망은 사람 두뇌의 신경세포인 뉴런이 전기신호를 전달하는 모습을 모방한 기계학습 모델이다.",
              "활성화 함수는 순 입력함수로부터 전달받은 값을 출력값으로 변환해 주는 함수이다."
            ],
            correctIndex: 0,
            explanationGPT: `이 문제의 목표는 인공신경망에 대한 정보 중 가장 잘못된 정보를 찾는 것입니다. 이를 통해, 4개의 선택지 중에서 가장 덜 정확한 것을 찾아야합니다. 이 문제를 해결하기 위해 계획은 다음과 같습니다:
<br><br>
1. 각 선택지를 각 개념에 대해 검증한다.
2. 그 중에서 하나가 다른 것들과 달리 잘못되었다는 것을 확인한다.
<br><br>
적용해보면,
<br><br>
1. "인공신경망에서 역전파는 입력층(Input Layer)에서 출력층(Output Layer)까지 정보가 전달되는 과정이다." - 이는 잘못된 정보입니다. 역전파는 신경망이 예측한 출력값과 실제 출력값의 차이, 즉 오차를 구한 후 이 오차를 출력층에서 입력층 방향으로 거꾸로 되돌려 보내 가중치를 조절하는 과정을 말합니다.
2. "인공신경망은 입력값을 받아서 출력값을 만들기 위해 활성화 함수를 사용한다." - 이는 정확한 정보입니다. 신경망의 각 뉴런은 활성화 함수를 포함하며, 이 함수는 뉴런의 출력값을 결정하는 역할을 합니다.
3. "인공신경망은 사람 두뇌의 신경세포인 뉴런이 전기신호를 전달하는 모습을 모방한 기계학습 모델이다." - 이는 정확한 정보입니다. 인공신경망은 생물학적 뉴런의 작동 원리를 모방하여 설계된 컴퓨터 시스템입니다.
4. "활성화 함수는 순 입력함수로부터 전달받은 값을 출력값으로 변환해 주는 함수이다." - 이는 정확한 정보입니다. 활성화 함수는 신경망 뉴런의 출력값을 결정하기 위해 사용됩니다.
<br><br>
따라서, 선택지 1번이 가장 오해를 불러일으키는 설명일 것입니다.`,
            explanationClaude: `이 문제를 해결하기 위한 계획:<br>
1. 각 선택지의 내용이 인공신경망의 특성과 일치하는지 검토
2. 잘못된 설명을 찾아내기
<br><br>
각 선택지 분석:
<br><br>
1. "역전파는 입력층에서 출력층까지 정보가 전달되는 과정이다."
- 이것은 잘못된 설명입니다.
- 역전파(Backpropagation)는 출력층에서 입력층 방향으로 오차를 전파하며 가중치를 조정하는 과정입니다.
- 입력층에서 출력층으로의 정보 전달은 순전파(Forward propagation)입니다.
<br><br>
2. "인공신경망은 입력값을 받아서 출력값을 만들기 위해 활성화 함수를 사용한다."
- 이는 정확한 설명입니다.
- 활성화 함수는 신경망의 각 뉴런에서 입력을 처리하여 출력을 생성하는 데 필수적입니다.
<br><br>
3. "인공신경망은 사람 두뇌의 신경세포인 뉴런이 전기신호를 전달하는 모습을 모방한 기계학습 모델이다."
- 이는 정확한 설명입니다.
- 인공신경망은 실제 생물학적 뉴런의 작동 방식을 모방하여 설계되었습니다.
<br><br>
4. "활성화 함수는 순 입력함수로부터 전달받은 값을 출력값으로 변환해 주는`
          },
          {
            question: "딥러닝의 트랜스포머(Transformer)의 구성요소로 가장 알맞지 않은 것은?",
            options: [
              "망각 게이트",
              "셀프 어텐션",
              "멀티헤드 셀프 어텐션",
              "포지셔널 인코딩"
            ],
            correctIndex: 0,
            explanationGPT: `해결 계획 : 딥러닝의 트랜스포머의 구성요소에 대해 이해하고, 선택지 중에서 가장 알맞지 않은 것을 구분합니다.
<br><br>
선택지 중 '망각 게이트', '셀프 어텐션', '멀티헤드 셀프 어텐션', '포지셔널 인코딩'에 대해 알아봅시다.
<br><br>
1. 망각 게이트: LSTM의 구성요소로, 셀 상태의 이전 정보를 얼마나 잊을지를 결정하는 역할을 한다. 
2. 셀프 어텐션: 트랜스포머의 중요한 구성요소로, 단어 간의 상호 관계에 따라 가중치를 다르게 부여하는 구성요소이다.
3. 멀티헤드 셀프 어텐션: 트랜스포머에서 사용되는 구성요소로, 셀프 어텐션을 여러번 수행하고 결과를 결합하는 것을 의미한다.
4. 포지셔널 인코딩: 트랜스포머에서 사용하는 구성요소로, 단어의 위치 정보를 주는 역할을 한다.
<br><br>
따라서 "망각 게이트"는 LSTM에서 사용되는 개념으로, 트랜스포머의 구성요소가 아니다.
<br><br>
답 : 1. 망각 게이트`,
            explanationClaude: `이 문제를 해결하기 위한 계획을 세워보겠습니다.
<br><br>
1. 트랜스포머의 주요 구성요소들을 나열해봅니다.
2. 각 보기가 트랜스포머의 구성요소인지 확인합니다.
3. 트랜스포머와 관련이 없는 요소를 찾아냅니다.
<br><br>
단계별 분석:
<br><br>
1. 트랜스포머의 주요 구성요소:
- 인코더와 디코더
- 셀프 어텐션 (Self-Attention)
- 멀티헤드 셀프 어텐션 (Multi-head Self-Attention)
- 포지셔널 인코딩 (Positional Encoding)
- 피드포워드 신경망
- Add & Norm (잔차 연결과 정규화)
<br><br>
2. 각 보기 분석:
- 망각 게이트: LSTM의 구성요소
- 셀프 어텐션: 트랜스포머의 핵심 구성요소
- 멀티헤드 셀프 어텐션: 트랜스포머의 핵심 구성요소
- 포지셔널 인코딩: 트랜스포머의 필수 구성요소
<br><br>
3. 결론:
'망각 게이트'는 LSTM(Long Short-Term Memory)의 구성요소이며, 트랜스포머의 구성요소가 아닙니다.
<br><br>
따라서 답은 1번 '망각 게이트'입니다.`
          }
        ],
        // 현재 문제 번호(0 ~ 6)
        currentQuestionIndex: 0,
        // 사용자가 고른 답안 저장용 배열 (null이면 아직 안 고름)
        userAnswers: []
      }
    },
    created() {
    // questions 개수만큼 userAnswers를 null로 초기화
    this.userAnswers = new Array(this.questions.length).fill(null)
  },
  computed: {
    totalQuestions() {
      return this.questions.length
    },
    currentQuestion() {
      return this.questions[this.currentQuestionIndex]
    },
    // 진행도(%) 계산
    progressPercentage() {
      return ((this.currentQuestionIndex + 1) / this.totalQuestions) * 100
    }
  },
  methods: {
    // 특정 보기 선택
    selectOption(optionIndex) {
      this.userAnswers[this.currentQuestionIndex] = optionIndex
    },
    // 다음 문제
    goNext() {
      if (this.currentQuestionIndex < this.totalQuestions - 1) {
        this.currentQuestionIndex++
      }
    },
    // 제출(채점) -> MainLayout으로 결과를 emit
    submitQuiz() {
      let correctCount = 0
      let incorrectList = []

      this.questions.forEach((q, i) => {
        const chosen = this.userAnswers[i]
        if (chosen === q.correctIndex) {
          correctCount++
        } else {
          // 틀린 문제 정보에 GPT/Claude 해설도 함께 담기
          incorrectList.push({
            questionIndex: i + 1,
            question: q.question,
            selected: chosen !== null ? q.options[chosen] : null,
            correct: q.options[q.correctIndex],
            explanationGPT: q.explanationGPT,
            explanationClaude: q.explanationClaude
          })
        }
      })

      // 예: 점수 = 맞힌 개수, 전체 문제 수
      const total = this.questions.length
      const result = {
        correctCount,
        total,
        incorrectList
      }

      // MainLayout에 finishQuiz 이벤트로 전달
      this.$emit('finishQuiz', result)
    }
  }
}
</script>
  
  
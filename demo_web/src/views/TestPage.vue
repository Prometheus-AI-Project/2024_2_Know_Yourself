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
        // 7개의 문제. question, 4개 options, 정답 인덱스 예시
        questions: [
          {
            question: "딥러닝에 대한 설명으로 옳은 것은?",
            options: [
              "오차역전파를 사용한다.",
              "ReLU보다 Sigmoid를 사용한다.",
              "딥러닝은 각 은닉층의 가중치를 통해 모형의 결과를 해석하기 용이하다.",
              "Dropout은 무작위 비율로 신경망을 제거한다."
            ], 
            correctIndex: 1
          },
          {
            question: "다음 중 자연어 처리(NLP) 기법으로 가장 적합하지 않은 것은?",
            options: [
              "ELMo",
              "GPT",
              "BERT",   
              "YOLO"
            ],
            correctIndex: 4
          },
          {
            question: "K-means 군집분석의 설명에 대해 옳은 것은?",
            options: [
              "초기 중심점 선택에 따라 결과가 달라질 수 있다.",
              "이상치에 민감하지 않다.",
              "범주형 변수에 대해 직접 적용이 가능하다.",
              "군집의 개수 K를 사전에 지정할 필요가 없다."
            ],
            correctIndex: 1
          },
          {
            question: "합성곱 신경망(CNN, Convolutional Neural Network)에 대한 설명으로 옳지 않은 것은?",
            options: [
              "이미지 분류 업무에 CNN을 활용할 수 있다.",
              "CNN 내부에는 여러 개의 합성곱(convolution)층과 풀링(pooling)층을 배치할 수 있다.",
              "CNN에서는 완전 연결(fully connected)층이 사용되지 않는다.",
              " CNN에서는 학습 데이터에 과적합(overfitting)되는 문제를 해결하기 위해 드롭아웃(dropout) 기법이 사용될 수 있다."
            ],
            correctIndex: 3
          },
          {
            question: "컴퓨터 비전 관련 딥러닝 모델에 대한 설명으로 옳지 않은 것은?",
            options: [
              "YOLO는 정확도보다 처리 속도에 강점을 갖는 객체 탐지 및 분류 모델이다.",
              "R-CNN 모델에서는 객체 탐지와 분류를 동시에 수행하므로 효율성이 높다.",
              "Fast R-CNN 모델에서는 입력 영상에서 객체를 탐지하기 위해 선택적 탐색 알고리즘을 사용한다.",
              "SSD(Single Shot Detector)는 YOLO에 비해 객체 탐지 및 분류의 정확도와 처리 속도가 개선된 모델이다."
            ],
            correctIndex: 2
          },
          {
            question: "인공신경망에 대한 설명으로 가장 알맞지 않은 것은?",
            options: [
              "인공신경망에서 역전파는 입력층(Input Layer)에서 출력층(Output Layer)까지 정보가 전달되는 과정이다.",
              "인공신경망은 입력값을 받아서 출력값을 만들기 위해 촬성화 함수를 사용한다.",
              "인공신경망은 사람 두뇌의 신경세포인 뉴런이 전기신호를 전달하는 모습을 모방한 기계학습 모델이다.",
              "활성화 함수는 순 입력함수로부터 전달받은 값을 출력값으로 변환해 주는 함수이다."
            ],
            correctIndex: 1
          },
          {
            question: "PCA에 대한 설명으로 옳지 않은 것은?",
            options: [
              "차원 축소는 고윳값이 낮은 순으로 정렬해서, 높은 고윳값을 가진 고유벡터만으로 데이터를 복원한다.",
              "변동 폭이 작은 축을 선택한다.",
              "축들은 서로 직교되어 있다.",
              "주성분은 상관성이 높은 변수들을 요약, 축소하는 기법이다."
            ],
            correctIndex: 2
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
      // 사용자가 선택지 클릭하면 해당 인덱스를 저장
      selectOption(optionIndex) {
        this.userAnswers[this.currentQuestionIndex] = optionIndex
      },
      // 다음 문제로 이동
      goNext() {
        if (this.currentQuestionIndex < this.totalQuestions - 1) {
          this.currentQuestionIndex++
        }
      },
      // 제출하기
      submitQuiz() {
        // 채점 예시
        let correctCount = 0
        this.questions.forEach((q, i) => {
          if (q.correctIndex === this.userAnswers[i]) {
            correctCount++
          }
        })
        alert(`총 ${this.totalQuestions}문제 중 ${correctCount}개 맞췄습니다!`)
  
        // 여기서 원하는 화면 전환이나 결과 페이지 이동 로직을 구현할 수 있음
      }
    }
  }
  </script>
  
  
<template>
  <div class="answer-wrapper">
    <!-- 상단에 '해설'이라는 큰 제목 -->
    <h1 class="title">Score</h1>

    <!-- 간단한 점수 안내 -->
    <div class="score-info">
      총 {{ quizResult.total }}문제 중 {{ quizResult.correctCount }}개 정답
      <span v-if="quizResult.total > 0">
        (정답률: {{ percentage }}%)
      </span>
    </div>

    <!-- 틀린 문제가 있는 경우 -->
    <div v-if="quizResult.incorrectList.length > 0" class="answer-container">
      <h2 class="sub-title">틀린 문제 해설</h2>

      <!-- 틀린 문제 목록 -->
      <div
        v-for="(item, idx) in quizResult.incorrectList"
        :key="idx"
        class="incorrect-item"
      >
        <h3>{{ item.questionIndex }}번 문제</h3>
        <p><strong>문제:</strong> {{ item.question }}</p>
        <p><strong>내 답:</strong> {{ item.selected || '미선택' }}</p>
        <p><strong>정답:</strong> {{ item.correct }}</p>

        <!-- 두 가지 해설(GPT, Claude) -->
        <div class="explanations">
          <div class="explanation-box">
            <h4>GPT 해설</h4>
            <p v-html="item.explanationGPT"></p>
          </div>
          <div class="explanation-box">
            <h4>Claude 해설</h4>
            <p v-html="item.explanationClaude"></p>
          </div>
        </div>

        <!-- 해설 선호도 선택(라디오 버튼) -->
        <div class="radio-group">
          <label>
            <input
              type="radio"
              :name="'betterAnswer-' + idx"
              value="gpt"
              v-model="userPreferredExplanations[idx]"
            />
            GPT 해설이 더 좋다
          </label>
          <label>
            <input
              type="radio"
              :name="'betterAnswer-' + idx"
              value="claude"
              v-model="userPreferredExplanations[idx]"
            />
            Claude 해설이 더 좋다
          </label>
        </div>

        <!-- 구분선 -->
        <hr />
      </div>

      <!-- 해설 선호 선택 완료 버튼 -->
      <div class="submit-area">
        <button @click="submitPreferences">해설 선호 선택 완료</button>
      </div>
    </div>

    <!-- 틀린 문제 없는 경우(모든 문제 정답) -->
    <div v-else class="all-correct">
      <p>모든 문제를 맞추셨네요! 축하드립니다!</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnswerPage',
  props: {
    // MainLayout에서 :quizResult="quizResult" 형태로 전달
    quizResult: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      // 각 틀린 문제별로 'gpt' 또는 'claude'를 저장할 배열
      userPreferredExplanations: []
    }
  },
  computed: {
    // 정답률(%) 계산
    percentage() {
      if (this.quizResult.total === 0) return 0
      return Math.round(
        (this.quizResult.correctCount / this.quizResult.total) * 100
      )
    }
  },
  created() {
    // 틀린 문제 개수만큼 null로 초기화
    const numIncorrect = this.quizResult.incorrectList.length
    this.userPreferredExplanations = new Array(numIncorrect).fill(null)
  },
  methods: {
    submitPreferences() {
      console.log('해설 선호 선택:', this.userPreferredExplanations)
      alert('해설 선호 선택을 완료했습니다!')
      // 필요하면 서버 전송, 다른 페이지 이동, etc.
    }
  }
}
</script>

<style scoped>
.answer-wrapper {
  height: 80vh; 

  /* 세로 스크롤 활성화 */
  overflow-y: auto; 
  background-color: #fff;
  width: 80%;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* 상단 타이틀 (해설) */
.title {
  font-size: 20px;
  margin-bottom: 10px;
}

/* 점수 안내 문구 */
.score-info {
  margin-bottom: 20px;
  font-size: 1.2em;
}

/* 흰색 박스 컨테이너 */
.answer-container {
  width: 100%;
  background-color: #ffffff;
  display: inline-block;
  padding: 20px;
  border-radius: 8px;
  text-align: left; /* 내부 컨텐츠는 왼쪽 정렬 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sub-title {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
}

/* 틀린 문제 하나하나 */
.incorrect-item {
  margin-bottom: 30px;
}

/* 해설 2개를 옆으로 나란히 배치 */
.explanations {
  display: flex;
  flex-wrap: wrap; /* 화면이 좁으면 자동 줄바꿈 */
  gap: 20px;
  margin: 15px 0;
}

.explanation-box {
  flex: 1;
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 5px;
}

/* 라디오 버튼 그룹 */
.radio-group {
  margin-top: 10px;
  display: flex;
  gap: 15px;
}

.submit-area {
  text-align: center;
  margin-top: 40px;
}

.submit-area button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

/* 모든 문제 정답일 때 */
.all-correct {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>

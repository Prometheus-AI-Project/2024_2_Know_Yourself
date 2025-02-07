<template>
  <div class="answer-wrapper">
    <h1 class="title">Score</h1>
    <div class="score-info">
      총 {{ quizResult.total }}문제 중 {{ quizResult.correctCount }}개 정답
      <span v-if="quizResult.total > 0">
        (정답률: {{ percentage }}%)
      </span>
    </div>
    <h2 class="sub-title">틀린 문제 해설</h2>

    <div v-if="quizResult.incorrectList.length > 0" class="answer-container">
      <div
        v-for="(item, idx) in quizResult.incorrectList"
        :key="idx"
        class="incorrect-item"
      >
        <h3>{{ item.questionIndex }}번 문제</h3>
        <p><strong>문제:</strong> {{ item.question }}</p>
        <p><strong>내 답:</strong> {{ item.selected || '미선택' }}</p>
        <p><strong>정답:</strong> {{ item.correct }}</p>

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
        <hr />
      </div>
      <div class="submit-area">
        <button @click="submitPreferences">해설 선호 선택 완료</button>
      </div>
    </div>
    <div v-else class="all-correct">
      <p>모든 문제를 맞추셨네요! 축하드립니다!</p>
    </div>

    <div v-if="showCompletedMessage" class="completion-message">
      해설 선호 선택이 완료되었습니다!
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnswerPage',
  props: {
    quizResult: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      userPreferredExplanations: [] 
    }
  },
  computed: {
    percentage() {
      if (this.quizResult.total === 0) return 0
      return Math.round(
        (this.quizResult.correctCount / this.quizResult.total) * 100
      )
    }
  },
  created() {
    const numIncorrect = this.quizResult.incorrectList.length
    this.userPreferredExplanations = new Array(numIncorrect).fill(null)
  },
  methods: {
    submitPreferences() {
      let gptCount = 0
      let claudeCount = 0
      this.userPreferredExplanations.forEach(choice => {
        if (choice === 'gpt') gptCount++
        else if (choice === 'claude') claudeCount++
      })

      const userName = localStorage.getItem('user') || 'Guest'

      const stored = localStorage.getItem('rankData')
      if (stored) {
        let data = JSON.parse(stored)
        const reversed = [...data].reverse()
        const found = reversed.find(item => item.name === userName)
        
        if (found) {
          const realIndex = data.indexOf(found)
          
          data[realIndex].gptCount = (data[realIndex].gptCount || 0) + gptCount
          data[realIndex].claudeCount = (data[realIndex].claudeCount || 0) + claudeCount

          localStorage.setItem('rankData', JSON.stringify(data))
        }
      }

      alert('해설 선호 선택을 완료했습니다!')
    }
  }
}
</script>

<style scoped>
.answer-wrapper {
  height: 80vh; 
  overflow-y: auto; 
  background-color: #fff;
  width: 80%;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.title {
  background-color: #ADCDC0;
  margin-bottom: 17px;
  font-size: 24px;
  border-radius: 10px; 
  padding: 10px 10px; 
}

.score-info {
  margin-bottom: 20px;
  font-size: 1.2em;
}

.answer-container {
  width: 100%;
  background-color: #ffffff;
  display: inline-block;
  padding: 20px;
  border-radius: 8px;
  text-align: left;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sub-title {
  margin-top: 0;
  margin-bottom: 20px;
  background-color: #ADCDC0;
  font-size: 24px;
  border-radius: 10px; 
  padding: 10px 10px; 
} 

.incorrect-item {
  margin-bottom: 30px;
}

.explanations {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 15px 0;
}

.explanation-box {
  flex: 1;
  background-color: #f8f8f8;
  padding: 15px;
  border-radius: 5px;
}

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

.all-correct {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>

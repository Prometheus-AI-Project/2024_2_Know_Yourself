<!-- src/views/TestPage.vue -->
<template>
    <div class="container">
      <h1>시험 문제</h1>
      <div>
        <!-- v-for로 질문 반복 렌더링 -->
        <div v-for="(q, index) in questions" :key="index">
          <p>{{ index+1 }}. {{ q.question }}</p>
          <input type="text" :placeholder="q.placeholder" v-model="userAnswers[index]" />
        </div>
      </div>
      <button @click="submitTest">채점하기</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TestPage',
    data() {
      return {
        questions: [
          // 여기에 시험 문제를 객체 형태로 작성
          // 예) { question: "Vue란 무엇인가?", placeholder: "정답 입력" }
        ],
        userAnswers: []
      }
    },
    mounted() {
      // questions 로드 후, userAnswers 배열 초기화
      this.userAnswers = this.questions.map(() => "")
    },
    methods: {
      submitTest() {
        // 채점 로직 (예: alert, console.log 등)
        alert("채점 완료!")
      }
    }
  }
  </script>
  
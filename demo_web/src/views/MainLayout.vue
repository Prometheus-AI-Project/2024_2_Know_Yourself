<template>
  <div class="page-layout">
    <!-- 사이드바 -->
    <div class="sidebar">
      <div>
        <div class="profile-section">
          <img src="/assets/profile.png" alt="Profile Picture" class="profile-img" />
          <h3 class="profile-name">{{ userName }}</h3>
        </div>
        <ul>
          <li @click="logout()" class="menu-item">
            <img src="/assets/logout.svg" alt="Logout Icon" class="icon" /> Logout
          </li>
          <li @click="changeContent('test')">Test</li>
          <li @click="changeContent('answer')">Answer</li>
          <li @click="changeContent('ranking')">Ranking</li>
        </ul>
      </div>
      <div class="logo">
        <img src="/assets/logo.png" alt="Logo">
      </div>
    </div>

    <!-- 우측 메인 콘텐츠 영역 -->
    <div class="content" id="content-area">
      <!-- 
        currentContent에 따라 TestPage, AnswerPage, RankingPage 중 하나를 표시.
        :quizResult="quizResult" -> AnswerPage에 props로 전달
        @finishQuiz -> TestPage에서 채점 후 결과를 이 레이아웃으로 전달받기
      -->
      <component
        :is="currentContent"
        :quizResult="quizResult"
        @finishQuiz="handleFinishQuiz"
      ></component>
    </div>
  </div>
</template>

<script>
import TestPage from './TestPage.vue'
import AnswerPage from './AnswerPage.vue'
import RankingPage from './RankingPage.vue'

export default {
  name: 'MainLayout',
  data() {
    return {
      userName: localStorage.getItem("user") || "Guest",
      // 기본 페이지: TestPage
      currentContent: 'TestPage',
      // 채점 후 받아올 퀴즈 결과 데이터(틀린 문제 목록, 점수 등)
      quizResult: null
    }
  },
  components: {
    TestPage,
    AnswerPage,
    RankingPage
  },
  methods: {
    // 사이드바에서 메뉴 클릭 시 페이지 전환
    changeContent(pageName) {
      // pageName에 맞춰 currentContent를 변경
      if (pageName === 'test') {
        this.currentContent = 'TestPage'
      } else if (pageName === 'answer') {
        this.currentContent = 'AnswerPage'
      } else if (pageName === 'ranking') {
        this.currentContent = 'RankingPage'
      }
    },
    // TestPage에서 채점(제출) 완료 이벤트 수신
    handleFinishQuiz(result) {
      // result 예: { score, correctCount, total, incorrectList: [...] }
      this.quizResult = result
      // 채점 후 자동으로 AnswerPage로 전환
      this.currentContent = 'AnswerPage'
    },
    // 로그아웃
    logout() {
      localStorage.removeItem("user")
      // 메인 레이아웃의 상위(App.vue)에게 welcome 페이지로 바꿔달라고 요청
      this.$emit('changePage', 'welcome')
    }
  }
}
</script>

<style scoped>
/* 필요하다면 사이드바/레이아웃 스타일 */
</style>

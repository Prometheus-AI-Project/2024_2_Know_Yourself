<template>
  <div class="page-layout">
]    <div class="sidebar">
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
      // result: { correctCount, total, incorrectList } 등
      this.quizResult = result
      // 1) 정답률 계산
      const ratio = (result.correctCount / result.total) * 100
      // 2) 현재 사용자 닉네임
      const userName = this.userName // 이미 localStorage.getItem("user") 등으로 저장된 값
      // 3) localStorage에 "rankData"라는 키로 랭킹 목록을 누적
      const storedData = JSON.parse(localStorage.getItem("rankData")) || []
      storedData.push({
        name: userName,
        correctCount: result.correctCount,
        total: result.total,
        ratio: ratio
      })
      localStorage.setItem("rankData", JSON.stringify(storedData))

      this.currentContent = 'AnswerPage'
    },
    logout() {
      localStorage.removeItem("user")
      this.$emit('changePage', 'welcome')
    }
  }
}
</script>

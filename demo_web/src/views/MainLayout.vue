<!-- src/views/MainLayout.vue -->
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
        <!-- 현재 선택된 페이지에 따라 다른 컴포넌트를 보여준다 -->
        <component :is="currentContent"></component>
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
        currentContent: 'TestPage'
      }
    },
    components: {
      TestPage,
      AnswerPage,
      RankingPage
    },
    methods: {
      changeContent(pageName) {
        if (pageName === 'test') {
          this.currentContent = 'TestPage'
        } else if (pageName === 'answer') {
          this.currentContent = 'AnswerPage'
        } else if (pageName === 'ranking') {
          this.currentContent = 'RankingPage'
        }
      },
      logout() {
        localStorage.removeItem("user")
        // 메인 레이아웃의 상위(App.vue)에게 welcome 페이지로 바꿔달라고 요청
        this.$emit('changePage', 'welcome')
      }
    }
  }
  </script>
  
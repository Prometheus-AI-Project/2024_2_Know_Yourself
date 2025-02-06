<!-- src/App.vue -->
<template>
  <!-- page 상태에 따라 다른 컴포넌트를 보여줌 -->
  <component
    :is="currentView"
    @changePage="changePage"
  ></component>
</template>

<script>
import WelcomePage from './views/WelcomePage.vue'
import RegisterPage from './views/RegisterPage.vue'
import MainLayout from './views/MainLayout.vue'

export default {
  name: 'App',
  data() {
    return {
      page: 'welcome', // 초기 페이지: welcome
    }
  },
  computed: {
    currentView() {
      if (this.page === 'welcome') return WelcomePage
      if (this.page === 'register') return RegisterPage
      return MainLayout // 나머지 경우 'main'으로 보고 MainLayout 보여줌
    }
  },
  methods: {
    changePage(newPage) {
      this.page = newPage
    }
  }
}
</script>

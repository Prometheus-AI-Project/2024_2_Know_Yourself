<!-- src/views/WelcomePage.vue -->
<template>
    <div class="welcome-container">
      <div>
        <h1>Know Yourself!</h1>
        <p>자네 인공지능을 좀 아는가</p>
        <!-- Vite에서는 public 폴더의 이미지 경로를 /assets/... 로 참조 -->
        <img src="/assets/welcome.png" alt="Welcome Image">
        <br />
        <button @click="goRegister">시작하기</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'WelcomePage',
    methods: {
      goRegister() {
        // App.vue (부모)에게 "register" 페이지로 바꿔달라고 이벤트 발신
        this.$emit('changePage', 'register')
      }
    }
  }
  </script>
  
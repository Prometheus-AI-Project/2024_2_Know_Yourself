<template>
    <div class="welcome-container">
      <div>
        <h1>Know Yourself!</h1>
        <p>자네 인공지능을 좀 아는가</p>
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
        this.$emit('changePage', 'register')
      }
    }
  }
  </script>
  
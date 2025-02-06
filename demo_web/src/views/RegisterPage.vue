<!-- src/views/NicknamePage.vue -->
<template>
    <div class="register-container">
      <div class="register-image">
        <img src="/assets/loginpage.png" alt="Nickname Image">
      </div>
      <div class="register-form">
        <h1>Enter Your Nickname</h1>
        <p>별명을 입력해주세요.</p>
        
        <!-- 별명 입력 -->
        <input type="text" v-model="nickname" placeholder="Nickname" required />
        
        <br /><br />
        <button @click="goToTest">Next</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NicknamePage',
    data() {
      return {
        nickname: ''
      }
    },
    methods: {
      goToTest() {
        if (this.nickname.trim().length === 0) {
          alert("별명을 입력해주세요.");
          return;
        }
        // localStorage에 별명을 저장
        localStorage.setItem('user', this.nickname);
        
        // 부모(App.vue)에게 "test" 페이지로 이동 요청
        this.$emit('changePage', 'test');
      }
    }
  }
  </script>
  
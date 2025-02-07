<template>
    <div class="register-container">
      <div class="register-image">
        <img src="/assets/loginpage.png" alt="Nickname Image">
      </div>
      <div class="register-form">
        <h1>Enter Your Nickname</h1>
        <p>별명을 입력해주세요.</p>
            <input type="text" v-model="nickname" placeholder="Nickname" required />
        <br /><br />
        <button @click="goToTest">시험보러가기</button>
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
        localStorage.setItem('user', this.nickname);
        this.$emit('changePage', 'test');
      }
    }
  }
  </script>
  
const app = document.getElementById("app");

// 공통 레이아웃
const mainLayout = (content) => `
  <div class="page-layout">
    <div class="sidebar">
      <div>
        <div class="profile">
          <img src="assets/profile.png" alt="Profile Picture">
          <h3>별명: ${localStorage.getItem("user") || "Guest"}</h3>
        </div>
        <ul>
          <li onclick="navigateContent('login')">Login</li>
          <li onclick="navigateContent('test')">Test</li>
          <li onclick="navigateContent('answer')">Answer</li>
          <li onclick="navigateContent('ranking')">Ranking</li>
        </ul>
      </div>
      <div class="logo">
        <img src="assets/logo.png" alt="Logo">
      </div>
    </div>
    <div class="content" id="content-area">
      ${content}
    </div>
  </div>
`;

// 콘텐츠별 페이지
const pages = {
  welcome: `
    <div class="welcome-container">
      <div>
        <h1>Know Yourself!</h1>
        <p>자네 인공지능을 좀 아는가</p>
        <img src="assets/welcome.png" alt="Welcome Image">
        <br/>
        <button onclick="navigate('register')">시작하기</button>
      </div>
    </div>
  `,
  register: `
    <div class="register-container">
      <div class="register-image">
        <img src="assets/loginpage.png" alt="Register Image">
      </div>
      <div class="register-form">
        <h1>Create Account</h1>
        <p>아이디와 비밀번호를 입력해주세요.</p>
        <form onsubmit="createAccount(event)">
          <input type="text" id="username" placeholder="Username" required>
          <input type="password" id="password" placeholder="Password" required>
          <button type="submit">Create Account</button>
        </form>
        <button id="start-button" onclick="navigate('test')">시작하기</button>
      </div>
    </div>
  `,
  test: `
    <div class="container">
      <h1>시험 문제</h1>
      <div id="questions">
        <!-- 질문이 여기에 동적으로 추가됨 -->
      </div>
      <button onclick="submitTest()">채점하기</button>
    </div>
  `,
  answer: `
    <div class="container">
      <h1>정답 페이지</h1>
      <p>정답 페이지 콘텐츠입니다.</p>
    </div>
  `,
  ranking: `
    <div class="container">
      <h1>랭킹 페이지</h1>
      <p>랭킹 페이지 콘텐츠입니다.</p>
    </div>
  `,
};

// 페이지 이동 함수
function navigate(page) {
  if (page === "welcome" || page === "register") {
    app.innerHTML = pages[page];
  } else {
    const content = pages[page] || pages.test;
    app.innerHTML = mainLayout(content);
    if (page === "test") loadQuestions();
  }
}

// 콘텐츠 변경 함수 (사이드바 클릭 시)
function navigateContent(content) {
  const contentArea = document.getElementById("content-area");
  contentArea.innerHTML = pages[content] || pages.test;
  if (content === "test") loadQuestions();
}

// 계정 생성 함수
function createAccount(event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username && password) {
    localStorage.setItem("user", username);

    // "시작하기" 버튼 표시
    const startButton = document.getElementById("start-button");
    startButton.style.display = "block";
  } else {
    alert("아이디와 비밀번호를 입력해주세요.");
  }
}


// 시험 문제 로드 함수
function loadQuestions() {
  const questions = [

  ];

  const questionContainer = document.getElementById("questions");
  questions.forEach((q, index) => {
    questionContainer.innerHTML += `
      <p>${index + 1}. ${q.question}</p>
      <input type="text" id="answer-${index}" placeholder="정답 입력">
    `;
  });
  window.questions = questions;
}

// 초기 페이지 로드
navigate("welcome");

<template>
  <div class="ranking-container">
    <div class="ranking-left">
      <h1 class="title">AI Ranking</h1>
      
      <div class="top-three">
        <div
          class="rank-card"
          v-for="i in 3"
          :key="i"
        >
          <div class="medal">
            <img
              :src="getMedalImage(i - 1)"
              alt="Medal"
              class="medal-icon"
            />
          </div>
          <img src="/assets/profile.png" alt="Profile" class="profile-img"/>
          
          <template v-if="topThree[i - 1]">
            <h3>{{ topThree[i - 1].name }}</h3>
            <p>
              {{ topThree[i - 1].ratio.toFixed(1) }}%
              ({{ topThree[i - 1].correctCount }}/{{ topThree[i - 1].total }})
            </p>
          </template>
          <template v-else>
            <h3>---</h3>
            <p>No Data</p>
          </template>
        </div>
      </div>

      <!-- 4위 이후 테이블 -->
      <div class="other-ranks">
        <h2>Others</h2>
        <table class="rank-table">
          <thead>
            <tr>
              <th>순위</th>
              <th>닉네임</th>
              <th>정답률</th>
              <th>맞힌 개수</th>
              <th>총 문제 수</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="others.length === 0">
              <td colspan="5">No Data</td>
            </tr>
            <tr
              v-else
              v-for="(user, index) in others"
              :key="index"
            >
              <td>{{ index + 4 }}위</td>
              <td>{{ user.name }}</td>
              <td>{{ user.ratio.toFixed(1) }}%</td>
              <td>{{ user.correctCount }}</td>
              <td>{{ user.total }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 오른쪽 GPT vs Claude 통계 섹션 -->
    <div class="ranking-right">
      <h2 class="titles">GPT vs Claude 응답 비교</h2>
      <p><strong>프롬프트: plan_and_solve </strong><br>(LLM 스스로 문제를 풀기 위한 계획을 세우게 하고, 해당 계획에 따라 문제를 풀도록 하는 프롬프트)</p>
      <p><em>"인공지능 전문가로서 다음 문제의 답을 구하세요. <br> 질문에 대한 답을 1부터 4까지의 선택지 중에 한 개만 골라서 대답해야 합니다. <br><br> 먼저 문제를 이해하고, 문제 해결을 위하여 계획을 세워보세요. 그 다음, 문제를 해결하기 위해 그 계획에 따라 단계별로 실행하세요."</em></p>
      <hr />
      <div class="gpt-claude-stats">
        <br>
        <!-- GPT 이미지 + 비율 -->
        <img src="/assets/gpt.png" alt="GPT" class="gpt-img" width="200px" />
        <p class="gpt-ratio">
          GPT 선호비율:
          <span v-if="totalGPT + totalClaude > 0">
            {{ gptPercentage }}%
          </span>
          <span v-else>0%</span>
        </p>

        <!-- 중앙 "VS" -->
        <div class="vs-text"> <br> VS <br> </div>
        <br>
        <!-- Claude 이미지 + 비율 -->
        <img src="/assets/claude.svg" alt="Claude" class="claude-img" width="200px"/>
        <p class="claude-ratio">
          Claude 선호비율:
          <span v-if="totalGPT + totalClaude > 0">
            {{ claudePercentage }}%
          </span>
          <span v-else>0%</span>
        </p>
      </div>
    <!-- 초기화 버튼 -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'RankingPage',
  data() {
    return {
      rankList: [],
      totalGPT: 0,      // 전체 GPT 선택 건수
      totalClaude: 0    // 전체 Claude 선택 건수
    }
  },
  computed: {
    // 상위 3명 (인덱스 0,1,2)
    topThree() {
      return this.rankList.slice(0, 3)
    },
    // 4등 이후
    others() {
      return this.rankList.slice(3)
    }
  },
  methods: {
    // 메달 아이콘
    getMedalImage(index) {
      if (index === 0) return '/assets/gold.png'
      if (index === 1) return '/assets/silver.png'
      if (index === 2) return '/assets/bronze.png'
      return ''
    }
  },
  mounted() {
    // localStorage에서 rankData 가져오기
    const stored = localStorage.getItem('rankData')
    if (stored) {
      let data = JSON.parse(stored)

      // 정답률 내림차순 정렬 (ratio가 없으면 0 처리)
      data.sort((a, b) => (b.ratio || 0) - (a.ratio || 0))

      // 랭킹 리스트 저장
      this.rankList = data

      // GPT/Claude 통계: 모든 사용자 gptCount/claudeCount 합
      let gptSum = 0
      let claudeSum = 0
      data.forEach(user => {
        gptSum += user.gptCount || 0
        claudeSum += user.claudeCount || 0
      })
      this.totalGPT = gptSum
      this.totalClaude = claudeSum
    }
  }
}
</script>

<style scoped>
.ranking-container {
  display: flex;
  width: 85%;
  gap: 20px;
  padding: 20px;
}

.ranking-left {
  flex: 3; 
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.ranking-right {
  flex: 1.5;
  background-color: #fff;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.gpt-claude-stats {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.vs-text {
  margin: 20px 0;
}

.title {
  background-color: #ADCDC0;
  margin-bottom: 17px;
  font-size: 24px;
  border-radius: 10px; 
  padding: 10px 10px;
}

.top-three {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}

.rank-card {
  background-color: #fff;
  width: 250px;
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  margin: 0 5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.medal-icon {
  width: 80px;
  height: 80px;
}

.profile-img {
  width: 80px;
  height: 70px;
  margin: 10px 0;
}

.other-ranks {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.rank-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.rank-table th,
.rank-table td {
  border-bottom: 1px solid #eee;
  padding: 8px;
  text-align: center;
}

.ratio-box {
  margin-top: 10px;
  background-color: #f2f2f2;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}
</style>

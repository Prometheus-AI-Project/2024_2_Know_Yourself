<template>
  <div class="ranking-wrapper">
    <h1 class="title">AI Ranking</h1>
    
    <!-- 상위 3명(또는 없는 경우 No Data로 표시) -->
    <div class="top-three">
      <!-- 3개의 rank-card를 고정 생성 -->
      <div
        class="rank-card"
        v-for="i in 3"
        :key="i"
      >
        <div class="medal">
          <img
            :src="getMedalImage(i-1)"
            alt="Medal"
            class="medal-icon"
          />
        </div>
        <img src="/assets/profile.png" alt="Profile" class="profile-img" />
        
        <!-- topThree 배열에서 i-1 인덱스가 존재하면 그 데이터 표시 -->
        <template v-if="topThree[i-1]">
          <h3>{{ topThree[i-1].name }}</h3>
          <p>
            {{ topThree[i-1].ratio.toFixed(1) }}%
            ({{ topThree[i-1].correctCount }}/{{ topThree[i-1].total }})
          </p>
        </template>
        <!-- 데이터가 없으면 placeholder 표시 -->
        <template v-else>
          <h3>---</h3>
          <p>No Data</p>
        </template>
      </div>
    </div>

    <!-- 4위 이후 랭킹 (항상 테이블 구조 유지) -->
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
          <!-- 만약 others.length === 0 이면, “No Data” 표시 한 줄 -->
          <tr v-if="others.length === 0">
            <td colspan="5">No Data</td>
          </tr>
          <!-- others가 있으면 반복 렌더링 -->
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
</template>

<script>
export default {
  name: 'RankingPage',
  data() {
    return {
      rankList: []
    }
  },
  computed: {
    // 상위 3명 (0,1,2 인덱스)
    topThree() {
      return this.rankList.slice(0, 3)
    },
    // 4등 이후
    others() {
      return this.rankList.slice(3)
    }
  },
  methods: {
    // index: 0=금, 1=은, 2=동 메달
    getMedalImage(index) {
      if (index === 0) return '/assets/gold.png'
      if (index === 1) return '/assets/silver.png'
      if (index === 2) return '/assets/bronze.png'
      return ''
    }
  },
  mounted() {
    // localStorage에서 rankData 불러오기
    const stored = localStorage.getItem('rankData')
    if (stored) {
      let data = JSON.parse(stored)
      // 정답률 내림차순 정렬
      data.sort((a, b) => b.ratio - a.ratio)
      this.rankList = data
    }
  }
}
</script>

<style scoped>
.ranking-wrapper {
  padding: 20px;
}
.title {
  margin-bottom: 20px;
  font-size: 24px;
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
  padding: 15px;
  border-radius: 8px;
  margin: 0 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.medal-icon {
  width: 100px;
  height: 100px;
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
</style>

<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon">
              <i class="el-icon-user"></i>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ totalEmployees }}</div>
              <div class="stats-label">总员工数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon male">
              <i class="el-icon-male"></i>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ maleEmployees }}</div>
              <div class="stats-label">男性员工</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon female">
              <i class="el-icon-female"></i>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ femaleEmployees }}</div>
              <div class="stats-label">女性员工</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon department">
              <i class="el-icon-office-building"></i>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ departmentCount }}</div>
              <div class="stats-label">部门数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header">
            <span>部门人员分布</span>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">
              <i class="el-icon-pie-chart"></i>
              <p>部门人员分布图表</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <div slot="header">
            <span>年龄分布</span>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">
              <i class="el-icon-bar-chart"></i>
              <p>年龄分布图表</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近添加的员工 -->
    <el-row :gutter="20" class="recent-row">
      <el-col :span="24">
        <el-card class="recent-card">
          <div slot="header">
            <span>最近添加的员工</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="$router.push('/employees')">
              查看全部
            </el-button>
          </div>
          <el-table :data="recentEmployees" style="width: 100%">
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="department" label="部门" width="120" />
            <el-table-column prop="gender" label="性别" width="80">
              <template slot-scope="scope">
                {{ scope.row.gender === 'male' ? '男' : '女' }}
              </template>
            </el-table-column>
            <el-table-column prop="age" label="年龄" width="80" />
            <el-table-column prop="phone" label="联系电话" width="150" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column label="操作" width="120">
              <template slot-scope="scope">
                <el-button type="text" size="small" @click="viewEmployee(scope.row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Dashboard',
  data() {
    return {
      mockData: {
        totalEmployees: 156,
        maleEmployees: 89,
        femaleEmployees: 67,
        departmentCount: 8,
        recentEmployees: [
          {
            id: 1,
            name: '张三',
            department: '技术部',
            position: '前端工程师',
            phone: '13800138001',
            email: 'zhangsan@company.com',
            createTime: '2024-01-15 10:30:00'
          },
          {
            id: 2,
            name: '李四',
            department: '人事部',
            position: 'HR专员',
            phone: '13800138002',
            email: 'lisi@company.com',
            createTime: '2024-01-14 14:20:00'
          },
          {
            id: 3,
            name: '王五',
            department: '财务部',
            position: '会计',
            phone: '13800138003',
            email: 'wangwu@company.com',
            createTime: '2024-01-13 09:15:00'
          }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['allEmployees']),
    totalEmployees() {
      return this.allEmployees.length || this.mockData.totalEmployees
    },
    maleEmployees() {
      return this.allEmployees.filter(emp => emp.gender === 'male').length || this.mockData.maleEmployees
    },
    femaleEmployees() {
      return this.allEmployees.filter(emp => emp.gender === 'female').length || this.mockData.femaleEmployees
    },
    departmentCount() {
      const departments = new Set(this.allEmployees.map(emp => emp.department))
      return departments.size || this.mockData.departmentCount
    },
    recentEmployees() {
      return this.allEmployees.slice(0, 5) || this.mockData.recentEmployees
    }
  },
  mounted() {
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['fetchEmployees']),
    viewEmployee(employee) {
      this.$router.push(`/employee/${employee.id}`)
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-card {
  height: 120px;
}

.stats-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 24px;
  color: white;
}

.stats-icon i {
  color: #409EFF;
}

.stats-icon.male i {
  color: #67C23A;
}

.stats-icon.female i {
  color: #E6A23C;
}

.stats-icon.department i {
  color: #F56C6C;
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.stats-label {
  font-size: 14px;
  color: #909399;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 300px;
}

.chart-container {
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #909399;
}

.chart-placeholder i {
  font-size: 48px;
  margin-bottom: 10px;
}

.chart-placeholder p {
  margin: 0;
  font-size: 14px;
}

.recent-card {
  margin-bottom: 20px;
}
</style> 
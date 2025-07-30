<template>
  <div class="salary-detail">
    <div class="page-header">
      <h2>工资详情</h2>
      <div class="header-actions">
        <el-button type="primary" @click="editSalary">
          <i class="el-icon-edit"></i>
          编辑
        </el-button>
        <el-button @click="$router.go(-1)">
          <i class="el-icon-arrow-left"></i>
          返回
        </el-button>
      </div>
    </div>

    <el-card class="detail-card" v-loading="loading">
      <div v-if="salary" class="salary-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="工资记录ID">
            {{ salary.id }}
          </el-descriptions-item>
          <el-descriptions-item label="员工姓名">
            {{ salary.employee_name }}
          </el-descriptions-item>
          <el-descriptions-item label="工资月份">
            {{ salary.month }}
          </el-descriptions-item>
          <el-descriptions-item label="基本工资">
            <span style="color: #67C23A; font-weight: bold;">
              ¥{{ salary.basic_salary?.toLocaleString() }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="加班费">
            <span style="color: #E6A23C; font-weight: bold;">
              ¥{{ salary.overtime_pay?.toLocaleString() }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="奖金">
            <span style="color: #F56C6C; font-weight: bold;">
              ¥{{ salary.bonus?.toLocaleString() }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="总工资">
            <span style="color: #409EFF; font-weight: bold; font-size: 16px;">
              ¥{{ salary.total_salary?.toLocaleString() }}
            </span>
          </el-descriptions-item>
        </el-descriptions>

        <!-- 工资构成图表 -->
        <div class="salary-chart">
          <h3>工资构成</h3>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card class="chart-card">
                <div class="chart-item">
                  <div class="chart-label">基本工资</div>
                  <div class="chart-value">¥{{ salary.basic_salary?.toLocaleString() }}</div>
                  <div class="chart-percentage">
                    {{ getPercentage(salary.basic_salary, salary.total_salary) }}%
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="chart-card">
                <div class="chart-item">
                  <div class="chart-label">加班费</div>
                  <div class="chart-value">¥{{ salary.overtime_pay?.toLocaleString() }}</div>
                  <div class="chart-percentage">
                    {{ getPercentage(salary.overtime_pay, salary.total_salary) }}%
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="chart-card">
                <div class="chart-item">
                  <div class="chart-label">奖金</div>
                  <div class="chart-value">¥{{ salary.bonus?.toLocaleString() }}</div>
                  <div class="chart-percentage">
                    {{ getPercentage(salary.bonus, salary.total_salary) }}%
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="primary" @click="editSalary">
            <i class="el-icon-edit"></i>
            编辑工资记录
          </el-button>
          <el-button type="danger" @click="deleteSalary">
            <i class="el-icon-delete"></i>
            删除工资记录
          </el-button>
          <el-button @click="$router.push('/salary')">
            <i class="el-icon-back"></i>
            返回列表
          </el-button>
        </div>
      </div>

      <div v-else-if="!loading" class="no-data">
        <el-empty description="工资记录不存在或已被删除">
          <el-button type="primary" @click="$router.push('/salary')">
            返回列表
          </el-button>
        </el-empty>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'SalaryDetail',
  data() {
    return {
      loading: false,
      salary: null
    }
  },
  async mounted() {
    await this.loadSalary()
  },
  methods: {
    ...mapActions(['fetchSalary', 'deleteSalary']),
    
    async loadSalary() {
      try {
        this.loading = true
        const salaryId = this.$route.params.id
        this.salary = await this.fetchSalary(salaryId)
      } catch (error) {
        console.error('加载工资记录失败:', error)
        this.$message.error('加载工资记录失败')
        this.salary = null
      } finally {
        this.loading = false
      }
    },
    
    editSalary() {
      this.$router.push(`/salary/${this.salary.id}/edit`)
    },
    
    async deleteSalary() {
      try {
        await this.$confirm(
          `确定要删除员工"${this.salary.employee_name}"在${this.salary.month}的工资记录吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deleteSalary(this.salary.id)
        this.$message.success('删除成功')
        this.$router.push('/salary')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除工资记录失败:', error)
        }
      }
    },
    
    getPercentage(part, total) {
      if (!total || total === 0) return 0
      return ((part / total) * 100).toFixed(1)
    }
  }
}
</script>

<style scoped>
.salary-detail {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.detail-card {
  max-width: 1000px;
  margin: 0 auto;
}

.salary-info {
  padding: 20px 0;
}

.salary-chart {
  margin-top: 30px;
}

.salary-chart h3 {
  margin-bottom: 20px;
  color: #303133;
}

.chart-card {
  text-align: center;
  padding: 20px;
}

.chart-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.chart-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.chart-percentage {
  font-size: 12px;
  color: #909399;
}

.action-buttons {
  margin-top: 30px;
  text-align: center;
}

.action-buttons .el-button {
  margin: 0 10px;
}

.no-data {
  padding: 40px 0;
  text-align: center;
}

.el-descriptions {
  margin-bottom: 20px;
}
</style> 
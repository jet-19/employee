<template>
  <div class="attendance-detail">
    <div class="page-header">
      <h2>考勤详情</h2>
      <div class="header-actions">
        <el-button type="primary" @click="editAttendance">
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
      <div v-if="attendance" class="attendance-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="考勤ID">
            {{ attendance.id }}
          </el-descriptions-item>
          <el-descriptions-item label="员工姓名">
            {{ attendance.employee_name }}
          </el-descriptions-item>
          <el-descriptions-item label="考勤日期">
            {{ attendance.date }}
          </el-descriptions-item>
          <el-descriptions-item label="考勤状态">
            <el-tag :type="getStatusType(attendance.status)">
              {{ getStatusText(attendance.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="上班时间">
            {{ attendance.check_in_time }}
          </el-descriptions-item>
          <el-descriptions-item label="下班时间">
            {{ attendance.check_out_time }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="primary" @click="editAttendance">
            <i class="el-icon-edit"></i>
            编辑考勤记录
          </el-button>
          <el-button type="danger" @click="handleDeleteAttendance">
            <i class="el-icon-delete"></i>
            删除考勤记录
          </el-button>
          <el-button @click="$router.push('/attendance')">
            <i class="el-icon-back"></i>
            返回列表
          </el-button>
        </div>
      </div>

      <div v-else-if="!loading" class="no-data">
        <el-empty description="考勤记录不存在或已被删除">
          <el-button type="primary" @click="$router.push('/attendance')">
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
  name: 'AttendanceDetail',
  data() {
    return {
      loading: false,
      attendance: null
    }
  },
  async mounted() {
    await this.loadAttendance()
  },
  methods: {
    ...mapActions(['fetchAttendance', 'deleteAttendance']),
    
    async loadAttendance() {
      try {
        this.loading = true
        const attendanceId = this.$route.params.id
        this.attendance = await this.fetchAttendance(attendanceId)
      } catch (error) {
        console.error('加载考勤记录失败:', error)
        this.$message.error('加载考勤记录失败')
        this.attendance = null
      } finally {
        this.loading = false
      }
    },
    
    editAttendance() {
      this.$router.push(`/attendance/${this.attendance.id}/edit`)
    },
    
    async handleDeleteAttendance() {
      try {
        await this.$confirm(
          `确定要删除员工"${this.attendance.employee_name}"在${this.attendance.date}的考勤记录吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deleteAttendance(this.attendance.id)
        this.$message.success('删除成功')
        this.$router.push('/attendance')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除考勤记录失败:', error)
        }
      }
    },
    
    getStatusType(status) {
      const statusMap = {
        'present': 'success',
        'absent': 'danger',
        'late': 'warning',
        'early_out': 'warning',
        'leave': 'info'
      }
      return statusMap[status] || 'info'
    },
    
    getStatusText(status) {
      const statusMap = {
        'present': '正常出勤',
        'absent': '缺勤',
        'late': '迟到',
        'early_out': '早退',
        'leave': '请假'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.attendance-detail {
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
  max-width: 800px;
  margin: 0 auto;
}

.attendance-info {
  padding: 20px 0;
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
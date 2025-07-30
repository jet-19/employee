<template>
  <div class="add-attendance">
    <div class="page-header">
      <h2>添加考勤记录</h2>
      <el-button @click="$router.go(-1)">
        <i class="el-icon-arrow-left"></i>
        返回
      </el-button>
    </div>

    <el-card class="form-card">
      <el-form
        ref="attendanceForm"
        :model="attendanceForm"
        :rules="formRules"
        label-width="120px"
        v-loading="submitting"
      >
        <el-form-item label="员工" prop="employee_id">
          <el-select
            v-model="attendanceForm.employee_id"
            placeholder="请选择员工"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="employee in allEmployees"
              :key="employee.id"
              :label="employee.name"
              :value="employee.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="考勤日期" prop="date">
          <el-date-picker
            v-model="attendanceForm.date"
            type="date"
            placeholder="选择考勤日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="上班时间" prop="check_in_time">
          <el-time-picker
            v-model="attendanceForm.check_in_time"
            placeholder="选择上班时间"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="下班时间" prop="check_out_time">
          <el-time-picker
            v-model="attendanceForm.check_out_time"
            placeholder="选择下班时间"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="考勤状态" prop="status">
          <el-select
            v-model="attendanceForm.status"
            placeholder="请选择考勤状态"
            style="width: 100%"
          >
            <el-option label="正常出勤" value="present" />
            <el-option label="缺勤" value="absent" />
            <el-option label="迟到" value="late" />
            <el-option label="早退" value="early_out" />
            <el-option label="请假" value="leave" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitting">
            <i class="el-icon-check"></i>
            保存
          </el-button>
          <el-button @click="resetForm">
            <i class="el-icon-refresh"></i>
            重置
          </el-button>
          <el-button @click="$router.go(-1)">
            <i class="el-icon-close"></i>
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'AddAttendance',
  data() {
    return {
      submitting: false,
      attendanceForm: {
        employee_id: null,
        date: '',
        check_in_time: '',
        check_out_time: '',
        status: ''
      },
      formRules: {
        employee_id: [
          { required: true, message: '请选择员工', trigger: 'change' }
        ],
        date: [
          { required: true, message: '请选择考勤日期', trigger: 'change' }
        ],
        check_in_time: [
          { required: true, message: '请选择上班时间', trigger: 'change' }
        ],
        check_out_time: [
          { required: true, message: '请选择下班时间', trigger: 'change' }
        ],
        status: [
          { required: true, message: '请选择考勤状态', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['allEmployees'])
  },
  mounted() {
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['createAttendance', 'fetchEmployees']),
    
    async submitForm() {
      try {
        const valid = await this.$refs.attendanceForm.validate()
        if (!valid) return
        
        this.submitting = true
        await this.createAttendance(this.attendanceForm)
        
        this.$message.success('考勤记录创建成功')
        this.$router.push('/attendance')
      } catch (error) {
        console.error('创建考勤记录失败:', error)
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.$refs.attendanceForm.resetFields()
    }
  }
}
</script>

<style scoped>
.add-attendance {
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

.form-card {
  max-width: 600px;
  margin: 0 auto;
}

.el-form-item {
  margin-bottom: 20px;
}
</style> 
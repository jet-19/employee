<template>
  <div class="edit-salary">
    <div class="page-header">
      <h2>编辑工资记录</h2>
      <el-button @click="$router.go(-1)">
        <i class="el-icon-arrow-left"></i>
        返回
      </el-button>
    </div>

    <el-card class="form-card" v-loading="loading">
      <el-form
        ref="salaryForm"
        :model="salaryForm"
        :rules="formRules"
        label-width="120px"
        v-loading="submitting"
      >
        <el-form-item label="员工" prop="employee_id">
          <el-select
            v-model="salaryForm.employee_id"
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

        <el-form-item label="工资月份" prop="month">
          <el-date-picker
            v-model="salaryForm.month"
            type="month"
            placeholder="选择工资月份"
            format="yyyy-MM"
            value-format="yyyy-MM-01"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="基本工资" prop="basic_salary">
          <el-input-number
            v-model="salaryForm.basic_salary"
            :min="0"
            :precision="2"
            :step="100"
            placeholder="请输入基本工资"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="加班费" prop="overtime_pay">
          <el-input-number
            v-model="salaryForm.overtime_pay"
            :min="0"
            :precision="2"
            :step="100"
            placeholder="请输入加班费"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="奖金" prop="bonus">
          <el-input-number
            v-model="salaryForm.bonus"
            :min="0"
            :precision="2"
            :step="100"
            placeholder="请输入奖金"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="总工资">
          <el-input
            :value="totalSalary"
            readonly
            style="width: 100%"
          >
            <template slot="prepend">¥</template>
          </el-input>
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
  name: 'EditSalary',
  data() {
    return {
      loading: false,
      submitting: false,
      salaryForm: {
        employee_id: null,
        month: '',
        basic_salary: 0,
        overtime_pay: 0,
        bonus: 0
      },
      formRules: {
        employee_id: [
          { required: true, message: '请选择员工', trigger: 'change' }
        ],
        month: [
          { required: true, message: '请选择工资月份', trigger: 'change' }
        ],
        basic_salary: [
          { required: true, message: '请输入基本工资', trigger: 'blur' },
          { type: 'number', min: 0, message: '基本工资不能为负数', trigger: 'blur' }
        ],
        overtime_pay: [
          { required: true, message: '请输入加班费', trigger: 'blur' },
          { type: 'number', min: 0, message: '加班费不能为负数', trigger: 'blur' }
        ],
        bonus: [
          { required: true, message: '请输入奖金', trigger: 'blur' },
          { type: 'number', min: 0, message: '奖金不能为负数', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['allEmployees']),
    totalSalary() {
      const basic = this.salaryForm.basic_salary || 0
      const overtime = this.salaryForm.overtime_pay || 0
      const bonus = this.salaryForm.bonus || 0
      return (basic + overtime + bonus).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    }
  },
  async mounted() {
    await this.loadSalary()
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['fetchSalary', 'updateSalary', 'fetchEmployees']),
    
    async loadSalary() {
      try {
        this.loading = true
        const salaryId = this.$route.params.id
        const salary = await this.fetchSalary(salaryId)
        
        this.salaryForm = {
          employee_id: salary.employee_id,
          month: salary.month,
          basic_salary: salary.basic_salary,
          overtime_pay: salary.overtime_pay,
          bonus: salary.bonus
        }
      } catch (error) {
        console.error('加载工资记录失败:', error)
        this.$message.error('加载工资记录失败')
        this.$router.push('/salary')
      } finally {
        this.loading = false
      }
    },
    
    async submitForm() {
      try {
        const valid = await this.$refs.salaryForm.validate()
        if (!valid) return
        
        this.submitting = true
        const salaryId = this.$route.params.id
        await this.updateSalary({
          id: salaryId,
          salaryData: this.salaryForm
        })
        
        this.$message.success('工资记录更新成功')
        this.$router.push('/salary')
      } catch (error) {
        console.error('更新工资记录失败:', error)
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.loadSalary()
    }
  }
}
</script>

<style scoped>
.edit-salary {
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
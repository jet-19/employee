<template>
  <div class="add-employee">
    <el-card class="form-card">
      <div slot="header">
        <span>添加员工</span>
      </div>
      
      <el-form
        ref="employeeForm"
        :model="employeeForm"
        :rules="formRules"
        label-width="120px"
        class="employee-form"
      >
        <!-- 基本信息 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="employeeForm.name" placeholder="请输入员工姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="employeeForm.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number 
                v-model="employeeForm.age" 
                :min="18" 
                :max="65" 
                placeholder="请输入年龄"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="employeeForm.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="employeeForm.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-select v-model="employeeForm.department" placeholder="请选择部门" style="width: 100%">
                <el-option label="技术部" value="技术部" />
                <el-option label="人事部" value="人事部" />
                <el-option label="财务部" value="财务部" />
                <el-option label="市场部" value="市场部" />
                <el-option label="运营部" value="运营部" />
                <el-option label="开发部" value="开发部" />
                <el-option label="行政部" value="行政部" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入职日期" prop="hire_date">
              <el-date-picker
                v-model="employeeForm.hire_date"
                type="date"
                placeholder="选择入职日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="基本工资" prop="salary">
              <el-input-number
                v-model="employeeForm.salary"
                :min="0"
                :precision="2"
                placeholder="请输入基本工资"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 操作按钮 -->
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">保存</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="$router.push('/employees')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'AddEmployee',
  data() {
    return {
      loading: false,
      employeeForm: {
        name: '',
        gender: 'male',
        age: 25,
        email: '',
        phone: '',
        department: '',
        hire_date: '',
        salary: 0
      },
      formRules: {
        name: [
          { required: true, message: '请输入员工姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '姓名长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ],
        hire_date: [
          { required: true, message: '请选择入职日期', trigger: 'change' }
        ],
        salary: [
          { required: true, message: '请输入基本工资', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['createEmployee']),
    
    async submitForm() {
      try {
        const valid = await this.$refs.employeeForm.validate()
        if (!valid) return
        
        this.loading = true
        
        await this.createEmployee(this.employeeForm)
        this.$router.push('/employees')
      } catch (error) {
        console.error('创建员工失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    resetForm() {
      this.$refs.employeeForm.resetFields()
    }
  }
}
</script>

<style scoped>
.add-employee {
  padding: 20px;
}

.form-card {
  max-width: 1200px;
  margin: 0 auto;
}

.employee-form {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}
</style> 
<template>
  <div class="employee-detail">
    <el-card class="detail-card">
      <div slot="header" class="card-header">
        <span>{{ isEdit ? '编辑员工信息' : '员工详情' }}</span>
        <div class="header-actions">
          <el-button v-if="!isEdit" type="primary" @click="startEdit">编辑</el-button>
          <el-button v-if="isEdit" type="success" @click="saveChanges" :loading="loading">保存</el-button>
          <el-button v-if="isEdit" @click="cancelEdit">取消</el-button>
          <el-button @click="$router.push('/employees')">返回</el-button>
        </div>
      </div>

      <el-form
        ref="employeeForm"
        :model="employeeForm"
        :rules="formRules"
        label-width="120px"
        class="employee-form"
        :disabled="!isEdit"
      >
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="员工ID">
              <el-input v-model="employeeForm.id" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="employeeForm.name" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="employeeForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="employeeForm.age" :min="18" :max="65" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="出生日期" prop="birthDate">
              <el-date-picker
                v-model="employeeForm.birthDate"
                type="date"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="婚姻状况" prop="maritalStatus">
              <el-select v-model="employeeForm.maritalStatus" style="width: 100%">
                <el-option label="未婚" value="未婚" />
                <el-option label="已婚" value="已婚" />
                <el-option label="离异" value="离异" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="身份证号" prop="idCard">
              <el-input v-model="employeeForm.idCard" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="employeeForm.phone" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="employeeForm.email" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="家庭住址" prop="address">
              <el-input v-model="employeeForm.address" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 工作信息 -->
        <el-divider content-position="left">工作信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="部门" prop="department">
              <el-select v-model="employeeForm.department" style="width: 100%">
                <el-option label="技术部" value="技术部" />
                <el-option label="人事部" value="人事部" />
                <el-option label="财务部" value="财务部" />
                <el-option label="市场部" value="市场部" />
                <el-option label="运营部" value="运营部" />
                <el-option label="行政部" value="行政部" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="职位" prop="position">
              <el-input v-model="employeeForm.position" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="员工状态" prop="status">
              <el-select v-model="employeeForm.status" style="width: 100%">
                <el-option label="在职" value="在职" />
                <el-option label="离职" value="离职" />
                <el-option label="试用期" value="试用期" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="入职日期" prop="hireDate">
              <el-date-picker
                v-model="employeeForm.hireDate"
                type="date"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="基本工资" prop="salary">
              <el-input-number
                v-model="employeeForm.salary"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="工作地点" prop="workLocation">
              <el-input v-model="employeeForm.workLocation" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 紧急联系人 -->
        <el-divider content-position="left">紧急联系人</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="紧急联系人" prop="emergencyContact">
              <el-input v-model="employeeForm.emergencyContact" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="紧急联系电话" prop="emergencyPhone">
              <el-input v-model="employeeForm.emergencyPhone" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="关系" prop="emergencyRelation">
              <el-input v-model="employeeForm.emergencyRelation" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 备注信息 -->
        <el-divider content-position="left">备注信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注" prop="remarks">
              <el-input
                v-model="employeeForm.remarks"
                type="textarea"
                :rows="4"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 系统信息 -->
        <el-divider content-position="left">系统信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="创建时间">
              <el-input v-model="employeeForm.createTime" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="更新时间">
              <el-input v-model="employeeForm.updateTime" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="操作人">
              <el-input v-model="employeeForm.operator" disabled />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'EmployeeDetail',
  data() {
    return {
      loading: false,
      isEdit: false,
      originalData: null,
      employeeForm: {
        id: '',
        name: '',
        gender: '男',
        age: 25,
        birthDate: '',
        maritalStatus: '未婚',
        idCard: '',
        phone: '',
        email: '',
        address: '',
        department: '',
        position: '',
        status: '在职',
        hireDate: '',
        salary: 0,
        workLocation: '',
        emergencyContact: '',
        emergencyPhone: '',
        emergencyRelation: '',
        remarks: '',
        createTime: '',
        updateTime: '',
        operator: 'admin'
      },
      formRules: {
        name: [
          { required: true, message: '请输入员工姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ],
        position: [
          { required: true, message: '请输入职位', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['allEmployees'])
  },
  mounted() {
    this.loadEmployeeData()
  },
  methods: {
    ...mapMutations(['UPDATE_EMPLOYEE']),
    
    loadEmployeeData() {
      const employeeId = parseInt(this.$route.params.id)
      const employee = this.allEmployees.find(emp => emp.id === employeeId)
      
      if (employee) {
        this.employeeForm = { ...employee }
        this.originalData = { ...employee }
      } else {
        // 模拟数据
        this.employeeForm = {
          id: employeeId,
          name: '张三',
          gender: '男',
          age: 28,
          birthDate: '1995-03-15',
          maritalStatus: '未婚',
          idCard: '110101199503151234',
          phone: '13800138001',
          email: 'zhangsan@company.com',
          address: '北京市朝阳区xxx街道xxx号',
          department: '技术部',
          position: '前端工程师',
          status: '在职',
          hireDate: '2023-01-15',
          salary: 12000,
          workLocation: '北京总部',
          emergencyContact: '张父',
          emergencyPhone: '13900139001',
          emergencyRelation: '父亲',
          remarks: '技术能力强，工作认真负责',
          createTime: '2023-01-15 10:30:00',
          updateTime: '2024-01-15 14:20:00',
          operator: 'admin'
        }
        this.originalData = { ...this.employeeForm }
      }
    },
    
    startEdit() {
      this.isEdit = true
    },
    
    async saveChanges() {
      try {
        const valid = await this.$refs.employeeForm.validate()
        if (!valid) return
        
        this.loading = true
        
        // 更新数据
        const updatedEmployee = {
          ...this.employeeForm,
          updateTime: new Date().toISOString()
        }
        
        this.UPDATE_EMPLOYEE(updatedEmployee)
        
        this.$message.success('保存成功')
        this.isEdit = false
        this.originalData = { ...updatedEmployee }
      } catch (error) {
        this.$message.error('保存失败，请重试')
      } finally {
        this.loading = false
      }
    },
    
    cancelEdit() {
      this.employeeForm = { ...this.originalData }
      this.isEdit = false
      this.$message.info('已取消编辑')
    }
  }
}
</script>

<style scoped>
.employee-detail {
  padding: 20px;
}

.detail-card {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.employee-form {
  margin-top: 20px;
}

.el-divider {
  margin: 30px 0 20px 0;
}

.el-form-item {
  margin-bottom: 20px;
}
</style> 
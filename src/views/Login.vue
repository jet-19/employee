<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>员工管理系统</h2>
        <p>{{ isLogin ? '欢迎登录' : '用户注册' }}</p>
      </div>
      
      <el-form
        ref="authForm"
        :model="authForm"
        :rules="authRules"
        class="auth-form"
        @submit.native.prevent="handleSubmit"
      >
        <el-form-item prop="username">
          <el-input
            v-model="authForm.username"
            prefix-icon="el-icon-user"
            placeholder="请输入用户名"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="authForm.password"
            prefix-icon="el-icon-lock"
            type="password"
            placeholder="请输入密码"
            size="large"
            @keyup.enter.native="handleSubmit"
          />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" prop="confirmPassword">
          <el-input
            v-model="authForm.confirmPassword"
            prefix-icon="el-icon-lock"
            type="password"
            placeholder="请确认密码"
            size="large"
            @keyup.enter.native="handleSubmit"
          />
        </el-form-item>
        
        <el-form-item v-if="!isLogin" prop="role">
          <el-select v-model="authForm.role" placeholder="请选择角色" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="submit-button"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ isLogin ? '登录' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <el-button type="text" @click="toggleMode">
          {{ isLogin ? '没有账号？立即注册' : '已有账号？立即登录' }}
        </el-button>
      </div>
      
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data() {
    // 密码确认验证
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.authForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      isLogin: true,
      loading: false,
      authForm: {
        username: '',
        password: '',
        confirmPassword: '',
        role: 'user'
      },
      authRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['login', 'register']),
    
    toggleMode() {
      this.isLogin = !this.isLogin
      this.resetForm()
    },
    
    resetForm() {
      this.authForm = {
        username: '',
        password: '',
        confirmPassword: '',
        role: 'user'
      }
      this.$refs.authForm && this.$refs.authForm.clearValidate()
    },
    
    async handleSubmit() {
      try {
        const valid = await this.$refs.authForm.validate()
        if (!valid) return
        
        this.loading = true
        
        if (this.isLogin) {
          // 登录
          await this.login({
            username: this.authForm.username,
            password: this.authForm.password
          })
          this.$message.success('登录成功')
          this.$router.push('/employees')
        } else {
          // 注册
          await this.register({
            username: this.authForm.username,
            password: this.authForm.password,
            role: this.authForm.role
          })
          this.isLogin = true
          this.resetForm()
        }
      } catch (error) {
        console.log(error);
        this.$message.error(error.response?.data?.message || error.message || '操作失败')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  width: 400px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #303133;
  margin-bottom: 10px;
  font-size: 28px;
  font-weight: 600;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.auth-form {
  margin-bottom: 20px;
}

.submit-button {
  width: 100%;
  height: 45px;
  font-size: 16px;
  font-weight: 500;
}

.auth-footer {
  text-align: center;
  margin-bottom: 20px;
}

.login-tips {
  text-align: center;
  color: #909399;
  font-size: 12px;
}

.login-tips p {
  margin: 5px 0;
}
</style> 
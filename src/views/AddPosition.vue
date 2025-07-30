<template>
  <div class="add-position">
    <div class="page-header">
      <h2>添加职位</h2>
      <el-button @click="$router.go(-1)">
        <i class="el-icon-arrow-left"></i>
        返回
      </el-button>
    </div>

    <el-card class="form-card">
      <el-form
        ref="positionForm"
        :model="positionForm"
        :rules="formRules"
        label-width="120px"
        v-loading="submitting"
      >
        <el-form-item label="职位名称" prop="name">
          <el-input
            v-model="positionForm.name"
            placeholder="请输入职位名称"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="职位描述" prop="description">
          <el-input
            v-model="positionForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入职位描述"
            maxlength="100"
            show-word-limit
          />
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
import { mapActions } from 'vuex'

export default {
  name: 'AddPosition',
  data() {
    return {
      submitting: false,
      positionForm: {
        name: '',
        description: ''
      },
      formRules: {
        name: [
          { required: true, message: '请输入职位名称', trigger: 'blur' },
          { min: 2, max: 100, message: '职位名称长度在 2 到 100 个字符', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入职位描述', trigger: 'blur' },
          { min: 5, max: 100, message: '职位描述长度在 5 到 100 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['createPosition']),
    
    async submitForm() {
      try {
        const valid = await this.$refs.positionForm.validate()
        if (!valid) return
        
        this.submitting = true
        await this.createPosition(this.positionForm)
        
        this.$message.success('职位创建成功')
        this.$router.push('/positions')
      } catch (error) {
        console.error('创建职位失败:', error)
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.$refs.positionForm.resetFields()
    }
  }
}
</script>

<style scoped>
.add-position {
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
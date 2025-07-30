<template>
  <div class="edit-position">
    <div class="page-header">
      <h2>编辑职位</h2>
      <el-button @click="$router.go(-1)">
        <i class="el-icon-arrow-left"></i>
        返回
      </el-button>
    </div>

    <el-card class="form-card" v-loading="loading">
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
  name: 'EditPosition',
  data() {
    return {
      loading: false,
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
  async mounted() {
    await this.loadPosition()
  },
  methods: {
    ...mapActions(['fetchPosition', 'updatePosition']),
    
    async loadPosition() {
      try {
        this.loading = true
        const positionId = this.$route.params.id
        const position = await this.fetchPosition(positionId)
        
        this.positionForm = {
          name: position.name,
          description: position.description
        }
      } catch (error) {
        console.error('加载职位信息失败:', error)
        this.$message.error('加载职位信息失败')
        this.$router.push('/positions')
      } finally {
        this.loading = false
      }
    },
    
    async submitForm() {
      try {
        const valid = await this.$refs.positionForm.validate()
        if (!valid) return
        
        this.submitting = true
        const positionId = this.$route.params.id
        await this.updatePosition({
          id: positionId,
          positionData: this.positionForm
        })
        
        this.$message.success('职位信息更新成功')
        this.$router.push('/positions')
      } catch (error) {
        console.error('更新职位失败:', error)
      } finally {
        this.submitting = false
      }
    },
    
    resetForm() {
      this.loadPosition()
    }
  }
}
</script>

<style scoped>
.edit-position {
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
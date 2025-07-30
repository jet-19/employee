<template>
  <div class="position-detail">
    <div class="page-header">
      <h2>职位详情</h2>
      <div class="header-actions">
        <el-button type="primary" @click="editPosition">
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
      <div v-if="position" class="position-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="职位ID">
            {{ position.id }}
          </el-descriptions-item>
          <el-descriptions-item label="职位名称">
            {{ position.name }}
          </el-descriptions-item>
          <el-descriptions-item label="职位描述" :span="2">
            {{ position.description }}
          </el-descriptions-item>
        </el-descriptions>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button type="primary" @click="editPosition">
            <i class="el-icon-edit"></i>
            编辑职位
          </el-button>
          <el-button type="danger" @click="handleDeletePosition">
            <i class="el-icon-delete"></i>
            删除职位
          </el-button>
          <el-button @click="$router.push('/positions')">
            <i class="el-icon-back"></i>
            返回列表
          </el-button>
        </div>
      </div>

      <div v-else-if="!loading" class="no-data">
        <el-empty description="职位不存在或已被删除">
          <el-button type="primary" @click="$router.push('/positions')">
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
  name: 'PositionDetail',
  data() {
    return {
      loading: false,
      position: null
    }
  },
  async mounted() {
    await this.loadPosition()
  },
  methods: {
    ...mapActions(['fetchPosition', 'deletePosition']),
    
    async loadPosition() {
      try {
        this.loading = true
        const positionId = this.$route.params.id
        this.position = await this.fetchPosition(positionId)
      } catch (error) {
        console.error('加载职位信息失败:', error)
        this.$message.error('加载职位信息失败')
        this.position = null
      } finally {
        this.loading = false
      }
    },
    
    editPosition() {
      this.$router.push(`/positions/${this.position.id}/edit`)
    },
    
    async handleDeletePosition() {
      try {
        await this.$confirm(
          `确定要删除职位"${this.position.name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deletePosition(this.position.id)
        this.$message.success('删除成功')
        this.$router.push('/positions')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除职位失败:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.position-detail {
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

.position-info {
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
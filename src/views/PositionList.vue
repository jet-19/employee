<template>
  <div class="position-list">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>职位管理</h2>
      <el-button type="primary" @click="$router.push('/positions/add')">
        <i class="el-icon-plus"></i>
        添加职位
      </el-button>
    </div>

    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.name"
            placeholder="搜索职位名称"
            clearable
            @clear="handleSearch"
            @keyup.enter.native="handleSearch"
          >
            <i slot="prefix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-input
            v-model="searchForm.description"
            placeholder="搜索职位描述"
            clearable
            @clear="handleSearch"
            @keyup.enter.native="handleSearch"
          >
            <i slot="prefix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="handleSearch">
            <i class="el-icon-search"></i>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <i class="el-icon-refresh"></i>
            重置
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 职位列表表格 -->
    <el-card class="table-card">
      <div slot="header">
        <span>职位列表</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="fetchPositions">
          <i class="el-icon-refresh"></i>
          刷新
        </el-button>
      </div>

      <el-table
        :data="paginatedPositions"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="职位名称" width="200" />
        <el-table-column prop="description" label="职位描述" />
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="viewPosition(scope.row)">
              <i class="el-icon-view"></i>
              查看
            </el-button>
            <el-button type="text" size="small" @click="editPosition(scope.row)">
              <i class="el-icon-edit"></i>
              编辑
            </el-button>
            <el-button type="text" size="small" @click="handleDeletePosition(scope.row)" style="color: #F56C6C">
              <i class="el-icon-delete"></i>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 批量操作 -->
      <div class="batch-actions" v-if="selectedPositions.length > 0">
        <el-button type="danger" size="small" @click="batchDelete">
          <i class="el-icon-delete"></i>
          批量删除 ({{ selectedPositions.length }})
        </el-button>
      </div>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredPositions.length"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'PositionList',
  data() {
    return {
      loading: false,
      searchForm: {
        name: '',
        description: ''
      },
      selectedPositions: [],
      pagination: {
        currentPage: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    ...mapGetters(['allPositions', 'isLoading']),
    filteredPositions() {
      let positions = this.allPositions

      // 按名称搜索
      if (this.searchForm.name) {
        positions = positions.filter(pos => 
          pos.name.toLowerCase().includes(this.searchForm.name.toLowerCase())
        )
      }

      // 按描述搜索
      if (this.searchForm.description) {
        positions = positions.filter(pos => 
          pos.description.toLowerCase().includes(this.searchForm.description.toLowerCase())
        )
      }

      return positions
    },
    paginatedPositions() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredPositions.slice(start, end)
    }
  },
  mounted() {
    this.fetchPositions()
  },
  methods: {
    ...mapActions(['fetchPositions', 'deletePosition']),
    
    handleSearch() {
      this.pagination.currentPage = 1
    },
    
    handleReset() {
      this.searchForm = {
        name: '',
        description: ''
      }
      this.pagination.currentPage = 1
    },
    
    handleSelectionChange(selection) {
      this.selectedPositions = selection
    },
    
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.pagination.currentPage = 1
    },
    
    handleCurrentChange(page) {
      this.pagination.currentPage = page
    },
    
    viewPosition(position) {
      this.$router.push(`/positions/${position.id}`)
    },
    
    editPosition(position) {
      this.$router.push(`/positions/${position.id}/edit`)
    },
    
    async handleDeletePosition(position) {
      try {
        await this.$confirm(
          `确定要删除职位"${position.name}"吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deletePosition(position.id)
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除职位失败:', error)
        }
      }
    },
    
    async batchDelete() {
      try {
        await this.$confirm(
          `确定要删除选中的 ${this.selectedPositions.length} 个职位吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const deletePromises = this.selectedPositions.map(position => 
          this.deletePosition(position.id)
        )
        
        await Promise.all(deletePromises)
        this.$message.success('批量删除成功')
        this.selectedPositions = []
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
        }
      }
    }
  }
}
</script>

<style scoped>
.position-list {
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

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.batch-actions {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style> 
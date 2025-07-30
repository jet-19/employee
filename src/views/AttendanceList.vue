<template>
  <div class="attendance-list">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>考勤管理</h2>
      <el-button type="primary" @click="$router.push('/attendance/add')">
        <i class="el-icon-plus"></i>
        添加考勤
      </el-button>
    </div>

    <!-- 搜索和筛选区域 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select
            v-model="searchForm.employee_id"
            placeholder="选择员工"
            clearable
            filterable
            @change="handleSearch"
          >
            <el-option
              v-for="employee in allEmployees"
              :key="employee.id"
              :label="employee.name"
              :value="employee.id"
            />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="searchForm.date_from"
            type="date"
            placeholder="开始日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            @change="handleSearch"
          />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="searchForm.date_to"
            type="date"
            placeholder="结束日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            @change="handleSearch"
          />
        </el-col>
        <el-col :span="6">
          <el-select
            v-model="searchForm.status"
            placeholder="考勤状态"
            clearable
            @change="handleSearch"
          >
            <el-option label="正常出勤" value="present" />
            <el-option label="缺勤" value="absent" />
            <el-option label="迟到" value="late" />
            <el-option label="早退" value="early_out" />
            <el-option label="请假" value="leave" />
          </el-select>
        </el-col>
      </el-row>
      <el-row :gutter="20" style="margin-top: 10px;">
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

    <!-- 考勤列表表格 -->
    <el-card class="table-card">
      <div slot="header">
        <span>考勤记录</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="fetchAttendances">
          <i class="el-icon-refresh"></i>
          刷新
        </el-button>
      </div>

      <el-table
        :data="paginatedAttendances"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="employee_name" label="员工姓名" width="120" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="check_in_time" label="上班时间" width="120" />
        <el-table-column prop="check_out_time" label="下班时间" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="viewAttendance(scope.row)">
              <i class="el-icon-view"></i>
              查看
            </el-button>
            <el-button type="text" size="small" @click="editAttendance(scope.row)">
              <i class="el-icon-edit"></i>
              编辑
            </el-button>
            <el-button type="text" size="small" @click="handleDeleteAttendance(scope.row)" style="color: #F56C6C">
              <i class="el-icon-delete"></i>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 批量操作 -->
      <div class="batch-actions" v-if="selectedAttendances.length > 0">
        <el-button type="danger" size="small" @click="batchDelete">
          <i class="el-icon-delete"></i>
          批量删除 ({{ selectedAttendances.length }})
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
          :total="filteredAttendances.length"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'AttendanceList',
  data() {
    return {
      loading: false,
      searchForm: {
        employee_id: null,
        date_from: '',
        date_to: '',
        status: ''
      },
      selectedAttendances: [],
      pagination: {
        currentPage: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    ...mapGetters(['allAttendances', 'allEmployees', 'isLoading']),
    filteredAttendances() {
      return this.allAttendances
    },
    paginatedAttendances() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredAttendances.slice(start, end)
    }
  },
  mounted() {
    this.fetchAttendances()
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['fetchAttendances', 'fetchEmployees', 'deleteAttendance']),
    
    handleSearch() {
      this.pagination.currentPage = 1
      this.fetchAttendances(this.searchForm)
    },
    
    handleReset() {
      this.searchForm = {
        employee_id: null,
        date_from: '',
        date_to: '',
        status: ''
      }
      this.pagination.currentPage = 1
      this.fetchAttendances()
    },
    
    handleSelectionChange(selection) {
      this.selectedAttendances = selection
    },
    
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.pagination.currentPage = 1
    },
    
    handleCurrentChange(page) {
      this.pagination.currentPage = page
    },
    
    viewAttendance(attendance) {
      this.$router.push(`/attendance/${attendance.id}`)
    },
    
    editAttendance(attendance) {
      this.$router.push(`/attendance/${attendance.id}/edit`)
    },
    
    async handleDeleteAttendance(attendance) {
      try {
        await this.$confirm(
          `确定要删除员工"${attendance.employee_name}"在${attendance.date}的考勤记录吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deleteAttendance(attendance.id)
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除考勤记录失败:', error)
        }
      }
    },
    
    async batchDelete() {
      try {
        await this.$confirm(
          `确定要删除选中的 ${this.selectedAttendances.length} 条考勤记录吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const deletePromises = this.selectedAttendances.map(attendance => 
          this.deleteAttendance(attendance.id)
        )
        
        await Promise.all(deletePromises)
        this.$message.success('批量删除成功')
        this.selectedAttendances = []
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
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
.attendance-list {
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
<template>
  <div class="salary-list">
    <!-- 页面标题和操作按钮 -->
    <div class="page-header">
      <h2>工资管理</h2>
      <el-button type="primary" @click="$router.push('/salary/add')">
        <i class="el-icon-plus"></i>
        添加工资
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
            v-model="searchForm.month_from"
            type="month"
            placeholder="开始月份"
            format="yyyy-MM"
            value-format="yyyy-MM-01"
            @change="handleSearch"
          />
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="searchForm.month_to"
            type="month"
            placeholder="结束月份"
            format="yyyy-MM"
            value-format="yyyy-MM-01"
            @change="handleSearch"
          />
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

    <!-- 工资列表表格 -->
    <el-card class="table-card">
      <div slot="header">
        <span>工资记录</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="fetchSalaries">
          <i class="el-icon-refresh"></i>
          刷新
        </el-button>
      </div>

      <el-table
        :data="paginatedSalaries"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="employee_name" label="员工姓名" width="120" />
        <el-table-column prop="month" label="工资月份" width="120" />
        <el-table-column prop="basic_salary" label="基本工资" width="120">
          <template slot-scope="scope">
            ¥{{ scope.row.basic_salary?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="overtime_pay" label="加班费" width="120">
          <template slot-scope="scope">
            ¥{{ scope.row.overtime_pay?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="bonus" label="奖金" width="120">
          <template slot-scope="scope">
            ¥{{ scope.row.bonus?.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="total_salary" label="总工资" width="120">
          <template slot-scope="scope">
            <span style="font-weight: bold; color: #409EFF;">
              ¥{{ scope.row.total_salary?.toLocaleString() }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="viewSalary(scope.row)">
              <i class="el-icon-view"></i>
              查看
            </el-button>
            <el-button type="text" size="small" @click="editSalary(scope.row)">
              <i class="el-icon-edit"></i>
              编辑
            </el-button>
            <el-button type="text" size="small" @click="handleDeleteSalary(scope.row)" style="color: #F56C6C">
              <i class="el-icon-delete"></i>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 批量操作 -->
      <div class="batch-actions" v-if="selectedSalaries.length > 0">
        <el-button type="danger" size="small" @click="batchDelete">
          <i class="el-icon-delete"></i>
          批量删除 ({{ selectedSalaries.length }})
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
          :total="filteredSalaries.length"
        />
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'SalaryList',
  data() {
    return {
      loading: false,
      searchForm: {
        employee_id: null,
        month_from: '',
        month_to: ''
      },
      selectedSalaries: [],
      pagination: {
        currentPage: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    ...mapGetters(['allSalaries', 'allEmployees', 'isLoading']),
    filteredSalaries() {
      return this.allSalaries
    },
    paginatedSalaries() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredSalaries.slice(start, end)
    }
  },
  mounted() {
    this.fetchSalaries()
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['fetchSalaries', 'fetchEmployees', 'deleteSalary']),
    
    handleSearch() {
      this.pagination.currentPage = 1
      this.fetchSalaries(this.searchForm)
    },
    
    handleReset() {
      this.searchForm = {
        employee_id: null,
        month_from: '',
        month_to: ''
      }
      this.pagination.currentPage = 1
      this.fetchSalaries()
    },
    
    handleSelectionChange(selection) {
      this.selectedSalaries = selection
    },
    
    handleSizeChange(size) {
      this.pagination.pageSize = size
      this.pagination.currentPage = 1
    },
    
    handleCurrentChange(page) {
      this.pagination.currentPage = page
    },
    
    viewSalary(salary) {
      this.$router.push(`/salary/${salary.id}`)
    },
    
    editSalary(salary) {
      this.$router.push(`/salary/${salary.id}/edit`)
    },
    
    async handleDeleteSalary(salary) {
      try {
        await this.$confirm(
          `确定要删除员工"${salary.employee_name}"在${salary.month}的工资记录吗？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await this.deleteSalary(salary.id)
        this.$message.success('删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除工资记录失败:', error)
        }
      }
    },
    
    async batchDelete() {
      try {
        await this.$confirm(
          `确定要删除选中的 ${this.selectedSalaries.length} 条工资记录吗？`,
          '确认批量删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const deletePromises = this.selectedSalaries.map(salary => 
          this.deleteSalary(salary.id)
        )
        
        await Promise.all(deletePromises)
        this.$message.success('批量删除成功')
        this.selectedSalaries = []
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
.salary-list {
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
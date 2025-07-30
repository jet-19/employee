<template>
  <div class="employee-list">
    <!-- 搜索和操作栏 -->
    <el-card class="search-card">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchForm.name"
            placeholder="搜索员工姓名"
            prefix-icon="el-icon-search"
            clearable
            @keyup.enter.native="handleSearch"
          />
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.department" placeholder="选择部门" clearable>
            <el-option label="技术部" value="技术部" />
            <el-option label="人事部" value="人事部" />
            <el-option label="财务部" value="财务部" />
            <el-option label="市场部" value="市场部" />
            <el-option label="运营部" value="运营部" />
            <el-option label="开发部" value="开发部" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchForm.gender" placeholder="选择性别" clearable>
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-col>
        <el-col :span="6" style="text-align: right">
          <el-button type="success" icon="el-icon-plus" @click="$router.push('/employee/add')">
            添加员工
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 员工表格 -->
    <el-card class="table-card">
      <el-table
        :data="filteredEmployees"
        v-loading="loading"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="gender" label="性别" width="80">
          <template slot-scope="scope">
            {{ scope.row.gender === 'male' ? '男' : '女' }}
          </template>
        </el-table-column>
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="salary" label="工资" width="120">
          <template slot-scope="scope">
            ¥{{ scope.row.salary }}
          </template>
        </el-table-column>
        <el-table-column prop="hire_date" label="入职日期" width="120" />
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="editEmployee(scope.row)">
              编辑
            </el-button>
            <el-button type="text" size="small" style="color: #F56C6C" @click="deleteEmployeeHandler(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredEmployees.length"
        />
      </div>
    </el-card>

    <!-- 批量操作 -->
    <div v-if="selectedEmployees.length > 0" class="batch-actions">
      <el-card>
        <span>已选择 {{ selectedEmployees.length }} 项</span>
        <el-button type="danger" size="small" @click="batchDelete">批量删除</el-button>
        <el-button size="small" @click="clearSelection">取消选择</el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'EmployeeList',
  data() {
    return {
      searchForm: {
        name: '',
        department: '',
        gender: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 20
      },
      selectedEmployees: [],
      loading: false
    }
  },
  computed: {
    ...mapGetters(['allEmployees', 'isLoading']),
    filteredEmployees() {
      let employees = this.allEmployees
      
      if (this.searchForm.name) {
        employees = employees.filter(emp => 
          emp.name.toLowerCase().includes(this.searchForm.name.toLowerCase())
        )
      }
      
      if (this.searchForm.department) {
        employees = employees.filter(emp => emp.department === this.searchForm.department)
      }
      
      if (this.searchForm.gender) {
        employees = employees.filter(emp => emp.gender === this.searchForm.gender)
      }
      
      return employees
    }
  },
  mounted() {
    this.fetchEmployees()
  },
  methods: {
    ...mapActions(['fetchEmployees', 'deleteEmployee']),
    
    handleSearch() {
      this.pagination.currentPage = 1
    },
    
    resetSearch() {
      this.searchForm = {
        name: '',
        department: '',
        gender: ''
      }
      this.pagination.currentPage = 1
    },
    
    handleSelectionChange(selection) {
      this.selectedEmployees = selection
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    
    viewEmployee(employee) {
      this.$router.push(`/employee/${employee.id}`)
    },
    
    editEmployee(employee) {
      this.$router.push(`/employee/${employee.id}/edit`)
    },
    
    async deleteEmployeeHandler(employee) {
      try {
        await this.$confirm(`确定要删除员工 ${employee.name} 吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await this.deleteEmployee(employee.id)
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除员工失败:', error)
        }
      }
    },
    
    async batchDelete() {
      try {
        await this.$confirm(`确定要删除选中的 ${this.selectedEmployees.length} 名员工吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        for (const employee of this.selectedEmployees) {
          await this.deleteEmployee(employee.id)
        }
        
        this.selectedEmployees = []
      } catch (error) {
        if (error !== 'cancel') {
          console.error('批量删除失败:', error)
        }
      }
    },
    
    clearSelection() {
      this.selectedEmployees = []
    }
  }
}
</script>

<style scoped>
.employee-list {
  padding: 20px;
}

.search-card {
  margin-bottom: 20px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.batch-actions .el-card {
  padding: 10px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
</style> 
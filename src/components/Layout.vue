<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h2>员工管理系统</h2>
      </div>
      <el-menu
        :default-active="$route.path"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/employees">
          <i class="el-icon-user"></i>
          <span slot="title">员工管理</span>
        </el-menu-item>
        <el-menu-item index="/positions">
          <i class="el-icon-suitcase"></i>
          <span slot="title">职位管理</span>
        </el-menu-item>
        <el-menu-item index="/attendance">
          <i class="el-icon-date"></i>
          <span slot="title">考勤管理</span>
        </el-menu-item>
        <el-menu-item index="/salary">
          <i class="el-icon-money"></i>
          <span slot="title">工资管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="$route.name !== 'Dashboard'">{{ getPageTitle() }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <i class="el-icon-user"></i>
              {{ currentUser ? currentUser.username : '管理员' }}
              <i class="el-icon-arrow-down"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Layout',
  computed: {
    ...mapGetters(['currentUser'])
  },
  methods: {
    ...mapActions(['logout']),
    getPageTitle() {
      const routeNames = {
        'EmployeeList': '员工管理',
        'AddEmployee': '添加员工',
        'EmployeeDetail': '员工详情',
        'PositionList': '职位管理',
        'AddPosition': '添加职位',
        'AttendanceList': '考勤管理',
        'AddAttendance': '添加考勤',
        'AttendanceDetail': '考勤详情',
        'SalaryList': '工资管理',
        'AddSalary': '添加工资',
        'SalaryDetail': '工资详情'
      }
      return routeNames[this.$route.name] || ''
    },
    handleCommand(command) {
      if (command === 'logout') {
        this.logout()
      }
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  color: #bfcbd9;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;
  color: #fff;
}

.logo h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-menu {
  border: none;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  cursor: pointer;
  color: #606266;
  font-size: 14px;
}

.user-info i {
  margin-right: 5px;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 
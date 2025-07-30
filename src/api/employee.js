import axios from 'axios'

// 配置axios
axios.defaults.baseURL = 'http://localhost:5000/api'
axios.defaults.withCredentials = true

// 员工相关API
export const employeeAPI = {
  // 获取所有员工
  getEmployees() {
    return axios.get('/employees')
  },

  // 获取单个员工
  getEmployee(id) {
    return axios.get(`/employees/${id}`)
  },

  // 创建员工
  createEmployee(data) {
    return axios.post('/employees/', data)
  },

  // 更新员工
  updateEmployee(id, data) {
    return axios.put(`/employees/${id}`, data)
  },

  // 删除员工
  deleteEmployee(id) {
    return axios.delete(`/employees/${id}`)
  }
}

// 职位相关API
export const positionAPI = {
  // 获取所有职位
  getPositions() {
    return axios.get('/positions')
  },

  // 获取单个职位
  getPosition(id) {
    return axios.get(`/positions/${id}`)
  },

  // 创建职位
  createPosition(data) {
    return axios.post('/positions/', data)
  },

  // 更新职位
  updatePosition(id, data) {
    return axios.put(`/positions/${id}`, data)
  },

  // 删除职位
  deletePosition(id) {
    return axios.delete(`/positions/${id}`)
  }
}

// 认证相关API
export const authAPI = {
  // 用户注册
  register(credentials) {
    return axios.post('/auth/register', credentials)
  },

  // 用户登录
  login(credentials) {
    return axios.post('/auth/login', credentials)
  },

  // 用户登出
  logout() {
    return axios.post('/auth/logout')
  },

  // 获取用户信息
  getProfile() {
    return axios.get('/auth/profile')
  }
}

// 考勤相关API
export const attendanceAPI = {
  // 获取所有考勤记录
  getAttendances(params = {}) {
    return axios.get('/attendance', { params })
  },

  // 获取单个考勤记录
  getAttendance(id) {
    return axios.get(`/attendance/${id}`)
  },

  // 创建考勤记录
  createAttendance(data) {
    return axios.post('/attendance/', data)
  },

  // 更新考勤记录
  updateAttendance(id, data) {
    return axios.put(`/attendance/${id}`, data)
  },

  // 删除考勤记录
  deleteAttendance(id) {
    return axios.delete(`/attendance/${id}`)
  }
}

// 工资相关API
export const salaryAPI = {
  // 获取所有工资记录
  getSalaries(params = {}) {
    return axios.get('/salary', { params })
  },

  // 获取单个工资记录
  getSalary(id) {
    return axios.get(`/salary/${id}`)
  },

  // 创建工资记录
  createSalary(data) {
    return axios.post('/salary/', data)
  },

  // 更新工资记录
  updateSalary(id, data) {
    return axios.put(`/salary/${id}`, data)
  },

  // 删除工资记录
  deleteSalary(id) {
    return axios.delete(`/salary/${id}`)
  }
} 
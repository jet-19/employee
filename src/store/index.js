import Vue from 'vue'
import Vuex from 'vuex'
import { authAPI, employeeAPI, positionAPI, attendanceAPI, salaryAPI } from '../api/employee'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    employees: [],
    positions: [],
    attendances: [],
    salaries: [],
    loading: false
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
    },
    SET_EMPLOYEES(state, employees) {
      state.employees = employees
    },
    SET_POSITIONS(state, positions) {
      state.positions = positions
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    ADD_EMPLOYEE(state, employee) {
      state.employees.push(employee)
    },
    UPDATE_EMPLOYEE(state, updatedEmployee) {
      const index = state.employees.findIndex(emp => emp.id === updatedEmployee.id)
      if (index !== -1) {
        state.employees.splice(index, 1, updatedEmployee)
      }
    },
    DELETE_EMPLOYEE(state, employeeId) {
      state.employees = state.employees.filter(emp => emp.id !== employeeId)
    },
    ADD_POSITION(state, position) {
      state.positions.push(position)
    },
    UPDATE_POSITION(state, updatedPosition) {
      const index = state.positions.findIndex(pos => pos.id === updatedPosition.id)
      if (index !== -1) {
        state.positions.splice(index, 1, updatedPosition)
      }
    },
    DELETE_POSITION(state, positionId) {
      state.positions = state.positions.filter(pos => pos.id !== positionId)
    },
    SET_ATTENDANCES(state, attendances) {
      state.attendances = attendances
    },
    ADD_ATTENDANCE(state, attendance) {
      state.attendances.push(attendance)
    },
    UPDATE_ATTENDANCE(state, updatedAttendance) {
      const index = state.attendances.findIndex(att => att.id === updatedAttendance.id)
      if (index !== -1) {
        state.attendances.splice(index, 1, updatedAttendance)
      }
    },
    DELETE_ATTENDANCE(state, attendanceId) {
      state.attendances = state.attendances.filter(att => att.id !== attendanceId)
    },
    SET_SALARIES(state, salaries) {
      state.salaries = salaries
    },
    ADD_SALARY(state, salary) {
      state.salaries.push(salary)
    },
    UPDATE_SALARY(state, updatedSalary) {
      const index = state.salaries.findIndex(sal => sal.id === updatedSalary.id)
      if (index !== -1) {
        state.salaries.splice(index, 1, updatedSalary)
      }
    },
    DELETE_SALARY(state, salaryId) {
      state.salaries = state.salaries.filter(sal => sal.id !== salaryId)
    }
  },
  actions: {
    async register({ commit }, credentials) {
      try {
        const response = await authAPI.register(credentials)
        if (response.data.status === 'success') {
          Vue.prototype.$message.success('注册成功，请登录')
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      } catch (error) {
        throw error
      }
    },
    
    async login({ commit }, credentials) {
      try {
        const response = await authAPI.login(credentials)
        if (response.data.status === 'success') {
          commit('SET_USER', response.data.data)
          return response.data
        } else {
          throw new Error(response.data.message)
        }
      } catch (error) {
        throw error
      }
    },
    
    async logout({ commit }) {
      try {
        await authAPI.logout()
        commit('SET_USER', null)
        Vue.prototype.$router.push('/login')
      } catch (error) {
        console.error('登出失败:', error)
        // 即使API调用失败，也清除本地状态
        commit('SET_USER', null)
        Vue.prototype.$router.push('/login')
      }
    },
    
    async getProfile({ commit }) {
      try {
        const response = await authAPI.getProfile()
        if (response.data.status === 'success') {
          commit('SET_USER', response.data.data)
          return response.data.data
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        commit('SET_USER', null)
        throw error
      }
    },
    
    // 获取所有员工
    async fetchEmployees({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await employeeAPI.getEmployees()
        if (response.data.status === 'success') {
          commit('SET_EMPLOYEES', response.data.data)
        }
      } catch (error) {
        console.error('获取员工列表失败:', error)
        Vue.prototype.$message.error('获取员工列表失败')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取单个员工
    async fetchEmployee({ commit }, employeeId) {
      try {
        const response = await employeeAPI.getEmployee(employeeId)
        if (response.data.status === 'success') {
          return response.data.data
        }
      } catch (error) {
        console.error('获取员工信息失败:', error)
        Vue.prototype.$message.error('获取员工信息失败')
        throw error
      }
    },
    
    // 创建员工
    async createEmployee({ commit }, employeeData) {
      try {
        const response = await employeeAPI.createEmployee(employeeData)
        if (response.data.status === 'success') {
          commit('ADD_EMPLOYEE', response.data.data)
          Vue.prototype.$message.success('员工创建成功')
          return response.data.data
        }
      } catch (error) {
        console.error('创建员工失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '创建员工失败')
        } else {
          Vue.prototype.$message.error('创建员工失败')
        }
        throw error
      }
    },
    
    // 更新员工
    async updateEmployee({ commit }, { id, employeeData }) {
      try {
        const response = await employeeAPI.updateEmployee(id, employeeData)
        if (response.data.status === 'success') {
          commit('UPDATE_EMPLOYEE', response.data.data)
          Vue.prototype.$message.success('员工信息更新成功')
          return response.data.data
        }
      } catch (error) {
        console.error('更新员工失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '更新员工失败')
        } else {
          Vue.prototype.$message.error('更新员工失败')
        }
        throw error
      }
    },
    
    // 删除员工
    async deleteEmployee({ commit }, employeeId) {
      try {
        const response = await employeeAPI.deleteEmployee(employeeId)
        if (response.data.status === 'success') {
          commit('DELETE_EMPLOYEE', employeeId)
          Vue.prototype.$message.success('员工删除成功')
        }
      } catch (error) {
        console.error('删除员工失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '删除员工失败')
        } else {
          Vue.prototype.$message.error('删除员工失败')
        }
        throw error
      }
    },
    
    // 获取所有职位
    async fetchPositions({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await positionAPI.getPositions()
        if (response.data.status === 'success') {
          commit('SET_POSITIONS', response.data.data)
        }
      } catch (error) {
        console.error('获取职位列表失败:', error)
        Vue.prototype.$message.error('获取职位列表失败')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取单个职位
    async fetchPosition({ commit }, positionId) {
      try {
        const response = await positionAPI.getPosition(positionId)
        if (response.data.status === 'success') {
          return response.data.data
        }
      } catch (error) {
        console.error('获取职位信息失败:', error)
        Vue.prototype.$message.error('获取职位信息失败')
        throw error
      }
    },
    
    // 创建职位
    async createPosition({ commit }, positionData) {
      try {
        const response = await positionAPI.createPosition(positionData)
        if (response.data.status === 'success') {
          commit('ADD_POSITION', response.data.data)
          Vue.prototype.$message.success('职位创建成功')
          return response.data.data
        }
      } catch (error) {
        console.error('创建职位失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '创建职位失败')
        } else {
          Vue.prototype.$message.error('创建职位失败')
        }
        throw error
      }
    },
    
    // 更新职位
    async updatePosition({ commit }, { id, positionData }) {
      try {
        const response = await positionAPI.updatePosition(id, positionData)
        if (response.data.status === 'success') {
          commit('UPDATE_POSITION', response.data.data)
          Vue.prototype.$message.success('职位信息更新成功')
          return response.data.data
        }
      } catch (error) {
        console.error('更新职位失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '更新职位失败')
        } else {
          Vue.prototype.$message.error('更新职位失败')
        }
        throw error
      }
    },
    
    // 删除职位
    async deletePosition({ commit }, positionId) {
      try {
        const response = await positionAPI.deletePosition(positionId)
        if (response.data.status === 'success') {
          commit('DELETE_POSITION', positionId)
          Vue.prototype.$message.success('职位删除成功')
        }
      } catch (error) {
        console.error('删除职位失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '删除职位失败')
        } else {
          Vue.prototype.$message.error('删除职位失败')
        }
        throw error
      }
    },
    
    // 获取所有考勤记录
    async fetchAttendances({ commit }, params = {}) {
      commit('SET_LOADING', true)
      try {
        const response = await attendanceAPI.getAttendances(params)
        if (response.data.status === 'success') {
          commit('SET_ATTENDANCES', response.data.data)
        }
      } catch (error) {
        console.error('获取考勤记录失败:', error)
        Vue.prototype.$message.error('获取考勤记录失败')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取单个考勤记录
    async fetchAttendance({ commit }, attendanceId) {
      try {
        const response = await attendanceAPI.getAttendance(attendanceId)
        if (response.data.status === 'success') {
          return response.data.data
        }
      } catch (error) {
        console.error('获取考勤记录失败:', error)
        Vue.prototype.$message.error('获取考勤记录失败')
        throw error
      }
    },
    
    // 创建考勤记录
    async createAttendance({ commit }, attendanceData) {
      try {
        const response = await attendanceAPI.createAttendance(attendanceData)
        if (response.data.status === 'success') {
          commit('ADD_ATTENDANCE', response.data.data)
          Vue.prototype.$message.success('考勤记录创建成功')
          return response.data.data
        }
      } catch (error) {
        console.error('创建考勤记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '创建考勤记录失败')
        } else {
          Vue.prototype.$message.error('创建考勤记录失败')
        }
        throw error
      }
    },
    
    // 更新考勤记录
    async updateAttendance({ commit }, { id, attendanceData }) {
      try {
        const response = await attendanceAPI.updateAttendance(id, attendanceData)
        if (response.data.status === 'success') {
          commit('UPDATE_ATTENDANCE', response.data.data)
          Vue.prototype.$message.success('考勤记录更新成功')
          return response.data.data
        }
      } catch (error) {
        console.error('更新考勤记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '更新考勤记录失败')
        } else {
          Vue.prototype.$message.error('更新考勤记录失败')
        }
        throw error
      }
    },
    
    // 删除考勤记录
    async deleteAttendance({ commit }, attendanceId) {
      try {
        const response = await attendanceAPI.deleteAttendance(attendanceId)
        if (response.data.status === 'success') {
          commit('DELETE_ATTENDANCE', attendanceId)
          Vue.prototype.$message.success('考勤记录删除成功')
        }
      } catch (error) {
        console.error('删除考勤记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '删除考勤记录失败')
        } else {
          Vue.prototype.$message.error('删除考勤记录失败')
        }
        throw error
      }
    },
    
    // 获取所有工资记录
    async fetchSalaries({ commit }, params = {}) {
      commit('SET_LOADING', true)
      try {
        const response = await salaryAPI.getSalaries(params)
        if (response.data.status === 'success') {
          commit('SET_SALARIES', response.data.data)
        }
      } catch (error) {
        console.error('获取工资记录失败:', error)
        Vue.prototype.$message.error('获取工资记录失败')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 获取单个工资记录
    async fetchSalary({ commit }, salaryId) {
      try {
        const response = await salaryAPI.getSalary(salaryId)
        if (response.data.status === 'success') {
          return response.data.data
        }
      } catch (error) {
        console.error('获取工资记录失败:', error)
        Vue.prototype.$message.error('获取工资记录失败')
        throw error
      }
    },
    
    // 创建工资记录
    async createSalary({ commit }, salaryData) {
      try {
        const response = await salaryAPI.createSalary(salaryData)
        if (response.data.status === 'success') {
          commit('ADD_SALARY', response.data.data)
          Vue.prototype.$message.success('工资记录创建成功')
          return response.data.data
        }
      } catch (error) {
        console.error('创建工资记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '创建工资记录失败')
        } else {
          Vue.prototype.$message.error('创建工资记录失败')
        }
        throw error
      }
    },
    
    // 更新工资记录
    async updateSalary({ commit }, { id, salaryData }) {
      try {
        const response = await salaryAPI.updateSalary(id, salaryData)
        if (response.data.status === 'success') {
          commit('UPDATE_SALARY', response.data.data)
          Vue.prototype.$message.success('工资记录更新成功')
          return response.data.data
        }
      } catch (error) {
        console.error('更新工资记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '更新工资记录失败')
        } else {
          Vue.prototype.$message.error('更新工资记录失败')
        }
        throw error
      }
    },
    
    // 删除工资记录
    async deleteSalary({ commit }, salaryId) {
      try {
        const response = await salaryAPI.deleteSalary(salaryId)
        if (response.data.status === 'success') {
          commit('DELETE_SALARY', salaryId)
          Vue.prototype.$message.success('工资记录删除成功')
        }
      } catch (error) {
        console.error('删除工资记录失败:', error)
        if (error.response && error.response.data) {
          Vue.prototype.$message.error(error.response.data.message || '删除工资记录失败')
        } else {
          Vue.prototype.$message.error('删除工资记录失败')
        }
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    allEmployees: state => state.employees,
    allPositions: state => state.positions,
    allAttendances: state => state.attendances,
    allSalaries: state => state.salaries,
    isLoading: state => state.loading
  }
}) 
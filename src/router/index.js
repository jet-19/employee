import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../components/Layout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: 'employees',
        name: 'EmployeeList',
        component: () => import('../views/EmployeeList.vue')
      },
      {
        path: 'employee/add',
        name: 'AddEmployee',
        component: () => import('../views/AddEmployee.vue')
      },
      {
        path: 'employee/:id',
        name: 'EmployeeDetail',
        component: () => import('../views/EmployeeDetail.vue')
      },
      {
        path: 'employee/:id/edit',
        name: 'EditEmployee',
        component: () => import('../views/EditEmployee.vue')
      },
      {
        path: 'positions',
        name: 'PositionList',
        component: () => import('../views/PositionList.vue')
      },
      {
        path: 'positions/add',
        name: 'AddPosition',
        component: () => import('../views/AddPosition.vue')
      },
      {
        path: 'positions/:id',
        name: 'PositionDetail',
        component: () => import('../views/PositionDetail.vue')
      },
      {
        path: 'positions/:id/edit',
        name: 'EditPosition',
        component: () => import('../views/EditPosition.vue')
      },
      {
        path: 'attendance',
        name: 'AttendanceList',
        component: () => import('../views/AttendanceList.vue')
      },
      {
        path: 'attendance/add',
        name: 'AddAttendance',
        component: () => import('../views/AddAttendance.vue')
      },
      {
        path: 'attendance/:id',
        name: 'AttendanceDetail',
        component: () => import('../views/AttendanceDetail.vue')
      },
      {
        path: 'attendance/:id/edit',
        name: 'EditAttendance',
        component: () => import('../views/EditAttendance.vue')
      },
      {
        path: 'salary',
        name: 'SalaryList',
        component: () => import('../views/SalaryList.vue')
      },
      {
        path: 'salary/add',
        name: 'AddSalary',
        component: () => import('../views/AddSalary.vue')
      },
      {
        path: 'salary/:id',
        name: 'SalaryDetail',
        component: () => import('../views/SalaryDetail.vue')
      },
      {
        path: 'salary/:id/edit',
        name: 'EditSalary',
        component: () => import('../views/EditSalary.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  if (to.path === '/login') {
    next()
    return
  }
  
  // 暂时跳过认证检查，直接允许访问
  next()
  
  // 检查用户是否已登录
  // const store = router.app.$store
  // if (!store.getters.isAuthenticated) {
  //   try {
  //     // 尝试获取用户信息
  //     await store.dispatch('getProfile')
  //     next()
  //   } catch (error) {
  //     // 获取用户信息失败，跳转到登录页
  //     next('/login')
  //   }
  // } else {
  //   next()
  // }
})

export default router 

# 基于 Flask + Vue.js 的员工信息管理系统

## 功能介绍

本平台采用 B/S 架构，后端基于主流的 Python Flask 框架开发，前端采用 Vue.js + Element UI 实现。系统功能模块丰富，支持企业级员工信息全流程管理。

**主要功能模块：**
- 用户认证（注册、登录、登出、权限管理）
- 员工管理（增删查改、详细信息、搜索、分页）
- 职位管理（增删查改、职位描述、唯一性校验）
- 考勤管理（增删查改、员工考勤、状态统计、日期筛选）
- 工资管理（增删查改、工资构成、月份筛选、金额统计）
- 仪表盘（数据总览、统计分析）

## 演示地址

> 暂无线上演示，如需体验请本地部署。

## 体验账号

> 默认管理员账号请在数据库 `users` 表中自行设置，或通过注册功能创建。

## 代码结构

- `back/` 目录为后端 Flask 项目
- `src/` 目录为前端 Vue.js 项目

## 部署运行

### 后端运行步骤

1. **安装 Python 3.8+**
2. **安装依赖**  
   进入 `back` 目录，执行：
   ```bash
   pip install -r requirements.txt
   ```
3. **安装 MySQL 5.7+ 数据库，并创建数据库**  
   创建数据库命令如下（请根据实际情况修改数据库名）：
   ```sql
   CREATE DATABASE IF NOT EXISTS employee_management DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
   ```
4. **配置数据库连接**  
   编辑 `back/app.py`，修改如下配置为你的数据库账号密码：
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://用户名:密码@localhost/employee_management'
   ```
5. **初始化数据表**  
   启动 Flask 服务时会自动创建表，无需手动导入 SQL。
6. **启动 Flask 服务**  
   在 `back` 目录下执行：
   ```bash
   python app.py
   ```
   默认端口为 5000。

### 前端运行步骤

1. **安装 Node.js 16+**
2. **安装依赖**  
   进入 `src` 目录，执行：
   ```bash
   npm install
   ```
3. **运行项目**
   ```bash
   npm run serve
   ```
   默认端口为 8080。

### 常见问题

- **前后端联调跨域问题？**  
  已在 Flask 端配置 CORS，支持本地开发环境跨域访问。

- **数据库连接失败？**  
  请检查 `app.py` 中数据库配置，确保账号、密码、端口、数据库名正确，MySQL 服务已启动。

- **依赖安装失败？**  
  建议使用国内镜像源安装 Python/npm 依赖。

- **如何设置管理员？**  
  可直接在 `users` 表插入一条 `role=admin` 的用户数据，或注册后手动修改角色。

- **如何修改前端 API 地址？**  
  编辑 `src/api/employee.js`，修改 `axios.defaults.baseURL` 为后端实际地址。

- **数据表结构？**  
  详见 `back/models.py`，所有表结构均以 SQLAlchemy ORM 形式定义。

## 技术栈

- **后端**：Flask、Flask-SQLAlchemy、Flask-CORS、PyMySQL
- **前端**：Vue.js、Vuex、Vue Router、Element UI、Axios

## 付费咨询

如需定制开发、部署支持或技术咨询，请联系：

- 微信：`your_wechat_id`
- 邮箱：`your_email@example.com`

---

> 本项目适合企业级员工管理、考勤工资管理等场景，支持二次开发和功能扩展。 

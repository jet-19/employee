# Flask 用户管理系统

基于Flask和MySQL的用户管理系统，提供登录注册功能。

## 功能特性

- 用户注册和登录
- 密码加密存储
- 用户角色管理（管理员/普通用户）
- Session会话管理
- 权限控制
- RESTful API设计

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置MySQL
确保MySQL服务正在运行，并执行数据库初始化脚本：
```bash
mysql -u root -p < back/init.sql
```

### 3. 初始化数据库
```bash
python init_db.py
```

### 4. 运行应用
```bash
python app.py
```

应用将在 http://localhost:5000 运行

## API接口

### 用户注册
```
POST /register
Content-Type: application/json

{
    "username": "newuser",
    "password": "password123",
    "role": "user"
}
```

### 用户登录
```
POST /login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

### 用户登出
```
POST /logout
```

### 获取用户信息
```
GET /profile
```

### 获取所有用户（管理员权限）
```
GET /users
```

## 默认用户账号

系统会自动创建以下默认用户：

- **管理员**: admin / admin123
- **普通用户**: user / user123

## 数据库配置

默认配置：
- 主机：localhost
- 用户：root
- 密码：password
- 数据库：employee_management

如需修改，请编辑 `app.py` 中的数据库连接字符串。

## 测试API

运行测试脚本验证功能：
```bash
python test_api.py
```

## 安全特性

- 密码使用werkzeug.security进行哈希加密
- Session管理用户登录状态
- 基于角色的权限控制
- 输入验证和错误处理 
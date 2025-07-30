CREATE DATABASE IF NOT EXISTS employee_management;

USE employee_management;

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS salary_records;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 员工ID
    name VARCHAR(100) NOT NULL, -- 员工姓名
    gender ENUM('male', 'female') NOT NULL, -- 员工性别
    age INT NOT NULL, -- 员工年龄
    email VARCHAR(100) NOT NULL, -- 员工邮箱
    phone VARCHAR(100) NOT NULL, -- 员工电话
    department VARCHAR(100) NOT NULL, -- 员工部门
    salary DECIMAL(10, 2) NOT NULL, -- 员工工资
    hire_date DATE NOT NULL -- 入职日期
);

INSERT INTO employees (name, gender, age, email, phone, department, salary, hire_date) VALUES
('张三', 'male', 25, 'zhangsan@example.com', '13800138000', '开发部', 10000, '2021-01-01'),
('李四', 'female', 26, 'lisi@example.com', '13800138001', '开发部', 10000, '2021-01-01'),
('王五', 'male', 27, 'wangwu@example.com', '13800138002', '开发部', 10000, '2021-01-01'),
('赵六', 'female', 28, 'zhaoliu@example.com', '13800138003', '开发部', 10000, '2021-01-01');

CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 部门ID
    name VARCHAR(100) NOT NULL, -- 部门名称
    location VARCHAR(100) NOT NULL -- 部门位置
);

INSERT INTO departments (name, location) VALUES
('开发部', '北京'),
('测试部', '上海'),
('运维部', '广州'),
('人事部', '深圳');


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 用户ID
    username VARCHAR(100) NOT NULL, -- 用户名
    password VARCHAR(100) NOT NULL, -- 密码
    role ENUM('admin', 'user') NOT NULL -- 用户角色
);

INSERT INTO users (username, password, role) VALUES
('admin', '123456', 'admin'),
('user', '123456', 'user');


CREATE TABLE IF NOT EXISTS positions (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 职位ID
    name VARCHAR(100) NOT NULL, -- 职位名称
    description VARCHAR(100) NOT NULL -- 职位描述
);

INSERT INTO positions (name, description) VALUES
('开发工程师', '负责开发和维护软件系统'),
('测试工程师', '负责测试和验证软件系统'),
('运维工程师', '负责维护和优化软件系统'),
('人事专员', '负责员工招聘和培训');

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 考勤ID
    employee_id INT NOT NULL, -- 员工ID
    date DATE NOT NULL, -- 考勤日期
    check_in_time TIME NOT NULL, -- 上班时间
    check_out_time TIME NOT NULL, -- 下班时间
    status ENUM('present', 'absent', 'late', 'early_out', 'leave') NOT NULL -- 考勤状态
);

INSERT INTO attendance (employee_id, date, check_in_time, check_out_time, status) VALUES
(1, '2021-01-01', '09:00:00', '18:00:00', 'present'),
(2, '2021-01-01', '09:00:00', '18:00:00', 'present'),
(3, '2021-01-01', '09:00:00', '18:00:00', 'present'),
(4, '2021-01-01', '09:00:00', '18:00:00', 'present');

CREATE TABLE IF NOT EXISTS salary_records (
    id INT AUTO_INCREMENT PRIMARY KEY, -- 工资记录ID
    employee_id INT NOT NULL, -- 员工ID
    month DATE NOT NULL, -- 工资月份
    basic_salary DECIMAL(10, 2) NOT NULL, -- 基本工资
    overtime_pay DECIMAL(10, 2) NOT NULL, -- 加班费
    bonus DECIMAL(10, 2) NOT NULL, -- 奖金
    total_salary DECIMAL(10, 2) NOT NULL -- 总工资
);
INSERT INTO salary_records (employee_id, month, basic_salary, overtime_pay, bonus, total_salary) VALUES
(1, '2021-01-01', 10000, 1000, 1000, 12000),
(2, '2021-01-01', 10000, 1000, 1000, 12000),
(3, '2021-01-01', 10000, 1000, 1000, 12000),
(4, '2021-01-01', 10000, 1000, 1000, 12000);

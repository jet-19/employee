from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 定义用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)  # 明文密码，长度改为50
    role = db.Column(db.Enum('admin', 'user'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

# 定义职位模型
class Position(db.Model):
    __tablename__ = 'positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

# 定义员工模型
class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('male', 'female'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.DECIMAL(10, 2), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'salary': float(self.salary) if self.salary else None,
            'hire_date': self.hire_date.strftime('%Y-%m-%d') if self.hire_date else None
        }

# 定义考勤模型
class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time, nullable=False)
    check_out_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.Enum('present', 'absent', 'late', 'early_out', 'leave'), nullable=False)
    
    # 关联员工
    employee = db.relationship('Employee', backref='attendances')
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'check_in_time': self.check_in_time.strftime('%H:%M:%S') if self.check_in_time else None,
            'check_out_time': self.check_out_time.strftime('%H:%M:%S') if self.check_out_time else None,
            'status': self.status
        }

# 定义工资记录模型
class Salary(db.Model):
    __tablename__ = 'salary_records'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Date, nullable=False)
    basic_salary = db.Column(db.DECIMAL(10, 2), nullable=False)
    overtime_pay = db.Column(db.DECIMAL(10, 2), nullable=False)
    bonus = db.Column(db.DECIMAL(10, 2), nullable=False)
    total_salary = db.Column(db.DECIMAL(10, 2), nullable=False)
    
    # 关联员工
    employee = db.relationship('Employee', backref='salaries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'month': self.month.strftime('%Y-%m-%d') if self.month else None,
            'basic_salary': float(self.basic_salary) if self.basic_salary else None,
            'overtime_pay': float(self.overtime_pay) if self.overtime_pay else None,
            'bonus': float(self.bonus) if self.bonus else None,
            'total_salary': float(self.total_salary) if self.total_salary else None
        } 
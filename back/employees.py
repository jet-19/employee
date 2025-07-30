from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, Employee

# 创建employees蓝图
employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

# 获取所有员工
@employees_bp.route('/', methods=['GET', 'OPTIONS'])
def get_employees():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        employees = Employee.query.all()
        
        return jsonify({
            'status': 'success',
            'data': [employee.to_dict() for employee in employees]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取单个员工
@employees_bp.route('/<int:employee_id>', methods=['GET', 'OPTIONS'])
def get_employee(employee_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'status': 'error',
                'message': '员工不存在'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': employee.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 创建员工
@employees_bp.route('/', methods=['POST', 'OPTIONS'])
def create_employee():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['name', 'gender', 'age', 'email', 'phone', 'department', 'salary', 'hire_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} 是必需的'
                }), 400
        
        # 验证性别字段
        if data['gender'] not in ['male', 'female']:
            return jsonify({
                'status': 'error',
                'message': '性别必须是 male 或 female'
            }), 400
        
        # 验证年龄
        try:
            age = int(data['age'])
            if age <= 0 or age > 150:
                return jsonify({
                    'status': 'error',
                    'message': '年龄必须在1-150之间'
                }), 400
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '年龄必须是数字'
            }), 400
        
        # 验证工资
        try:
            salary = float(data['salary'])
            if salary < 0:
                return jsonify({
                    'status': 'error',
                    'message': '工资不能为负数'
                }), 400
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '工资必须是数字'
            }), 400
        
        # 验证日期格式
        try:
            hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '入职日期格式错误，请使用 YYYY-MM-DD 格式'
            }), 400
        
        new_employee = Employee(
            name=data['name'],
            gender=data['gender'],
            age=age,
            email=data['email'],
            phone=data['phone'],
            department=data['department'],
            salary=salary,
            hire_date=hire_date
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '员工创建成功',
            'data': new_employee.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 更新员工
@employees_bp.route('/<int:employee_id>', methods=['PUT', 'OPTIONS'])
def update_employee(employee_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'status': 'error',
                'message': '员工不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'name' in data:
            employee.name = data['name']
        if 'gender' in data:
            if data['gender'] not in ['male', 'female']:
                return jsonify({
                    'status': 'error',
                    'message': '性别必须是 male 或 female'
                }), 400
            employee.gender = data['gender']
        if 'age' in data:
            try:
                age = int(data['age'])
                if age <= 0 or age > 150:
                    return jsonify({
                        'status': 'error',
                        'message': '年龄必须在1-150之间'
                    }), 400
                employee.age = age
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '年龄必须是数字'
                }), 400
        if 'email' in data:
            employee.email = data['email']
        if 'phone' in data:
            employee.phone = data['phone']
        if 'department' in data:
            employee.department = data['department']
        if 'salary' in data:
            try:
                salary = float(data['salary'])
                if salary < 0:
                    return jsonify({
                        'status': 'error',
                        'message': '工资不能为负数'
                    }), 400
                employee.salary = salary
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '工资必须是数字'
                }), 400
        if 'hire_date' in data:
            try:
                hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
                employee.hire_date = hire_date
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '入职日期格式错误，请使用 YYYY-MM-DD 格式'
                }), 400
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '员工信息更新成功',
            'data': employee.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 删除员工
@employees_bp.route('/<int:employee_id>', methods=['DELETE', 'OPTIONS'])
def delete_employee(employee_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({
                'status': 'error',
                'message': '员工不存在'
            }), 404
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '员工删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 
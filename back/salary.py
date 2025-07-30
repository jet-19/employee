from flask import Blueprint, request, jsonify, session
from datetime import datetime, date
from models import db, Salary, Employee

# 创建salary蓝图
salary_bp = Blueprint('salary', __name__, url_prefix='/api/salary')

# 获取所有工资记录
@salary_bp.route('/', methods=['GET', 'OPTIONS'])
def get_salaries():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        # 获取查询参数
        employee_id = request.args.get('employee_id', type=int)
        month_from = request.args.get('month_from')
        month_to = request.args.get('month_to')
        
        # 构建查询
        query = Salary.query
        
        if employee_id:
            query = query.filter(Salary.employee_id == employee_id)
        
        if month_from:
            try:
                month_from_obj = datetime.strptime(month_from, '%Y-%m-%d').date()
                query = query.filter(Salary.month >= month_from_obj)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '月份格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        if month_to:
            try:
                month_to_obj = datetime.strptime(month_to, '%Y-%m-%d').date()
                query = query.filter(Salary.month <= month_to_obj)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '月份格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        salaries = query.order_by(Salary.month.desc(), Salary.employee_id).all()
        
        return jsonify({
            'status': 'success',
            'data': [salary.to_dict() for salary in salaries]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取单个工资记录
@salary_bp.route('/<int:salary_id>', methods=['GET', 'OPTIONS'])
def get_salary(salary_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        salary = Salary.query.get(salary_id)
        
        if not salary:
            return jsonify({
                'status': 'error',
                'message': '工资记录不存在'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': salary.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 创建工资记录
@salary_bp.route('/', methods=['POST', 'OPTIONS'])
def create_salary():
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
        required_fields = ['employee_id', 'month', 'basic_salary', 'overtime_pay', 'bonus']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} 是必需的'
                }), 400
        
        # 验证员工是否存在
        employee = Employee.query.get(data['employee_id'])
        if not employee:
            return jsonify({
                'status': 'error',
                'message': '员工不存在'
            }), 400
        
        # 验证月份格式
        try:
            salary_month = datetime.strptime(data['month'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '月份格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        # 验证工资字段
        try:
            basic_salary = float(data['basic_salary'])
            overtime_pay = float(data['overtime_pay'])
            bonus = float(data['bonus'])
            
            if basic_salary < 0 or overtime_pay < 0 or bonus < 0:
                return jsonify({
                    'status': 'error',
                    'message': '工资金额不能为负数'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': '工资金额格式错误'
            }), 400
        
        # 计算总工资
        total_salary = basic_salary + overtime_pay + bonus
        
        # 检查是否已存在该员工该月份的工资记录
        existing_salary = Salary.query.filter_by(
            employee_id=data['employee_id'],
            month=salary_month
        ).first()
        
        if existing_salary:
            return jsonify({
                'status': 'error',
                'message': '该员工在该月份已有工资记录'
            }), 400
        
        new_salary = Salary(
            employee_id=data['employee_id'],
            month=salary_month,
            basic_salary=basic_salary,
            overtime_pay=overtime_pay,
            bonus=bonus,
            total_salary=total_salary
        )
        
        db.session.add(new_salary)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '工资记录创建成功',
            'data': new_salary.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 更新工资记录
@salary_bp.route('/<int:salary_id>', methods=['PUT', 'OPTIONS'])
def update_salary(salary_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        salary = Salary.query.get(salary_id)
        
        if not salary:
            return jsonify({
                'status': 'error',
                'message': '工资记录不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'employee_id' in data:
            # 验证员工是否存在
            employee = Employee.query.get(data['employee_id'])
            if not employee:
                return jsonify({
                    'status': 'error',
                    'message': '员工不存在'
                }), 400
            salary.employee_id = data['employee_id']
        
        if 'month' in data:
            try:
                salary_month = datetime.strptime(data['month'], '%Y-%m-%d').date()
                salary.month = salary_month
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '月份格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        # 更新工资字段
        basic_salary = salary.basic_salary
        overtime_pay = salary.overtime_pay
        bonus = salary.bonus
        
        if 'basic_salary' in data:
            try:
                basic_salary = float(data['basic_salary'])
                if basic_salary < 0:
                    return jsonify({
                        'status': 'error',
                        'message': '基本工资不能为负数'
                    }), 400
                salary.basic_salary = basic_salary
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': '基本工资格式错误'
                }), 400
        
        if 'overtime_pay' in data:
            try:
                overtime_pay = float(data['overtime_pay'])
                if overtime_pay < 0:
                    return jsonify({
                        'status': 'error',
                        'message': '加班费不能为负数'
                    }), 400
                salary.overtime_pay = overtime_pay
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': '加班费格式错误'
                }), 400
        
        if 'bonus' in data:
            try:
                bonus = float(data['bonus'])
                if bonus < 0:
                    return jsonify({
                        'status': 'error',
                        'message': '奖金不能为负数'
                    }), 400
                salary.bonus = bonus
            except (ValueError, TypeError):
                return jsonify({
                    'status': 'error',
                    'message': '奖金格式错误'
                }), 400
        
        # 重新计算总工资
        salary.total_salary = basic_salary + overtime_pay + bonus
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '工资记录更新成功',
            'data': salary.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 删除工资记录
@salary_bp.route('/<int:salary_id>', methods=['DELETE', 'OPTIONS'])
def delete_salary(salary_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        salary = Salary.query.get(salary_id)
        
        if not salary:
            return jsonify({
                'status': 'error',
                'message': '工资记录不存在'
            }), 404
        
        db.session.delete(salary)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '工资记录删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 
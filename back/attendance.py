from flask import Blueprint, request, jsonify, session
from datetime import datetime, date, time
from models import db, Attendance, Employee

# 创建attendance蓝图
attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

# 获取所有考勤记录
@attendance_bp.route('/', methods=['GET', 'OPTIONS'])
def get_attendances():
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
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        status = request.args.get('status')
        
        # 构建查询
        query = Attendance.query
        
        if employee_id:
            query = query.filter(Attendance.employee_id == employee_id)
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Attendance.date >= date_from_obj)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '日期格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Attendance.date <= date_to_obj)
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '日期格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        if status:
            if status not in ['present', 'absent', 'late', 'early_out', 'leave']:
                return jsonify({
                    'status': 'error',
                    'message': '无效的考勤状态'
                }), 400
            query = query.filter(Attendance.status == status)
        
        attendances = query.order_by(Attendance.date.desc(), Attendance.employee_id).all()
        
        return jsonify({
            'status': 'success',
            'data': [attendance.to_dict() for attendance in attendances]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取单个考勤记录
@attendance_bp.route('/<int:attendance_id>', methods=['GET', 'OPTIONS'])
def get_attendance(attendance_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        attendance = Attendance.query.get(attendance_id)
        
        if not attendance:
            return jsonify({
                'status': 'error',
                'message': '考勤记录不存在'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': attendance.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 创建考勤记录
@attendance_bp.route('/', methods=['POST', 'OPTIONS'])
def create_attendance():
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
        required_fields = ['employee_id', 'date', 'check_in_time', 'check_out_time', 'status']
        for field in required_fields:
            if field not in data or not data[field]:
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
        
        # 验证日期格式
        try:
            attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '日期格式错误，请使用YYYY-MM-DD格式'
            }), 400
        
        # 验证时间格式
        try:
            check_in_time = datetime.strptime(data['check_in_time'], '%H:%M:%S').time()
            check_out_time = datetime.strptime(data['check_out_time'], '%H:%M:%S').time()
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': '时间格式错误，请使用HH:MM:SS格式'
            }), 400
        
        # 验证考勤状态
        valid_statuses = ['present', 'absent', 'late', 'early_out', 'leave']
        if data['status'] not in valid_statuses:
            return jsonify({
                'status': 'error',
                'message': f'考勤状态必须是以下之一: {", ".join(valid_statuses)}'
            }), 400
        
        # 检查是否已存在该员工该日期的考勤记录
        existing_attendance = Attendance.query.filter_by(
            employee_id=data['employee_id'],
            date=attendance_date
        ).first()
        
        if existing_attendance:
            return jsonify({
                'status': 'error',
                'message': '该员工在该日期已有考勤记录'
            }), 400
        
        new_attendance = Attendance(
            employee_id=data['employee_id'],
            date=attendance_date,
            check_in_time=check_in_time,
            check_out_time=check_out_time,
            status=data['status']
        )
        
        db.session.add(new_attendance)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '考勤记录创建成功',
            'data': new_attendance.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 更新考勤记录
@attendance_bp.route('/<int:attendance_id>', methods=['PUT', 'OPTIONS'])
def update_attendance(attendance_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        attendance = Attendance.query.get(attendance_id)
        
        if not attendance:
            return jsonify({
                'status': 'error',
                'message': '考勤记录不存在'
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
            attendance.employee_id = data['employee_id']
        
        if 'date' in data:
            try:
                attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                attendance.date = attendance_date
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '日期格式错误，请使用YYYY-MM-DD格式'
                }), 400
        
        if 'check_in_time' in data:
            try:
                check_in_time = datetime.strptime(data['check_in_time'], '%H:%M:%S').time()
                attendance.check_in_time = check_in_time
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '时间格式错误，请使用HH:MM:SS格式'
                }), 400
        
        if 'check_out_time' in data:
            try:
                check_out_time = datetime.strptime(data['check_out_time'], '%H:%M:%S').time()
                attendance.check_out_time = check_out_time
            except ValueError:
                return jsonify({
                    'status': 'error',
                    'message': '时间格式错误，请使用HH:MM:SS格式'
                }), 400
        
        if 'status' in data:
            valid_statuses = ['present', 'absent', 'late', 'early_out', 'leave']
            if data['status'] not in valid_statuses:
                return jsonify({
                    'status': 'error',
                    'message': f'考勤状态必须是以下之一: {", ".join(valid_statuses)}'
                }), 400
            attendance.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '考勤记录更新成功',
            'data': attendance.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 删除考勤记录
@attendance_bp.route('/<int:attendance_id>', methods=['DELETE', 'OPTIONS'])
def delete_attendance(attendance_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        attendance = Attendance.query.get(attendance_id)
        
        if not attendance:
            return jsonify({
                'status': 'error',
                'message': '考勤记录不存在'
            }), 404
        
        db.session.delete(attendance)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '考勤记录删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 
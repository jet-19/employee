from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import os

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于session加密

# 配置CORS - 简化配置
CORS(app, 
     supports_credentials=True, 
     origins="*",
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers="*")

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入并初始化数据库
from models import db, User, Employee
db.init_app(app)

# 导入并注册auth蓝图
from auth import auth_bp
app.register_blueprint(auth_bp)

# 导入并注册employees蓝图
from employees import employees_bp
app.register_blueprint(employees_bp)

# 导入并注册positions蓝图
from positions import positions_bp
app.register_blueprint(positions_bp)

# 导入并注册attendance蓝图
from attendance import attendance_bp
app.register_blueprint(attendance_bp)

# 导入并注册salary蓝图
from salary import salary_bp
app.register_blueprint(salary_bp)

# 获取所有用户（仅管理员）
@app.route('/api/users', methods=['GET', 'OPTIONS'])
def get_users():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录且是管理员
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        if session.get('role') != 'admin':
            return jsonify({
                'status': 'error',
                'message': '权限不足'
            }), 403
        
        users = User.query.all()
        return jsonify({
            'status': 'success',
            'data': [user.to_dict() for user in users]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 根路径
@app.route('/')
def home():
    return jsonify({
        'message': 'Flask 用户管理系统',
        'status': 'success',
        'endpoints': {
            'register': 'POST /api/auth/register - 用户注册',
            'login': 'POST /api/auth/login - 用户登录',
            'logout': 'POST /api/auth/logout - 用户登出',
            'profile': 'GET /api/auth/profile - 获取用户信息',
            'users': 'GET /api/users - 获取所有用户（管理员）',
            'employees': 'GET /api/employees - 获取所有员工',
            'employee': 'GET /api/employees/<id> - 获取单个员工',
            'create_employee': 'POST /api/employees - 创建员工',
            'update_employee': 'PUT /api/employees/<id> - 更新员工',
            'delete_employee': 'DELETE /api/employees/<id> - 删除员工',
            'positions': 'GET /api/positions - 获取所有职位',
            'position': 'GET /api/positions/<id> - 获取单个职位',
            'create_position': 'POST /api/positions - 创建职位',
            'update_position': 'PUT /api/positions/<id> - 更新职位',
            'delete_position': 'DELETE /api/positions/<id> - 删除职位',
            'attendance': 'GET /api/attendance - 获取所有考勤记录',
            'attendance_detail': 'GET /api/attendance/<id> - 获取单个考勤记录',
            'create_attendance': 'POST /api/attendance - 创建考勤记录',
            'update_attendance': 'PUT /api/attendance/<id> - 更新考勤记录',
            'delete_attendance': 'DELETE /api/attendance/<id> - 删除考勤记录',
            'salary': 'GET /api/salary - 获取所有工资记录',
            'salary_detail': 'GET /api/salary/<id> - 获取单个工资记录',
            'create_salary': 'POST /api/salary - 创建工资记录',
            'update_salary': 'PUT /api/salary/<id> - 更新工资记录',
            'delete_salary': 'DELETE /api/salary/<id> - 删除工资记录'
        }
    })

# 测试CORS的路由
@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_cors():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    return jsonify({
        'status': 'success',
        'message': 'CORS测试成功',
        'data': {'test': 'cors'}
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000) 
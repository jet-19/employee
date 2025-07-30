from flask import Blueprint, request, jsonify, session
from datetime import datetime
from models import db, User

# 创建auth蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 用户注册
@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'status': 'error',
                'message': '用户名和密码是必需的'
            }), 400
        
        username = data['username']
        password = data['password']
        role = data.get('role', 'user')  # 默认为普通用户
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({
                'status': 'error',
                'message': '用户名已存在'
            }), 400
        
        # 创建新用户 - 明文存储密码
        new_user = User(
            username=username,
            password=password,  # 直接存储明文密码
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '注册成功',
            'data': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 用户登录
@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'status': 'error',
                'message': '用户名和密码是必需的'
            }), 400
        
        username = data['username']
        password = data['password']
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        # 直接比较明文密码
        if not user or user.password != password:
            return jsonify({
                'status': 'error',
                'message': '用户名或密码错误'
            }), 401
        
        # 登录成功，设置session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        
        return jsonify({
            'status': 'success',
            'message': '登录成功',
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 用户登出
@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 清除session
        session.clear()
        return jsonify({
            'status': 'success',
            'message': '登出成功'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取当前用户信息
@auth_bp.route('/profile', methods=['GET', 'OPTIONS'])
def get_profile():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        user_id = session['user_id']
        user = User.query.get(user_id)
        
        if not user:
            session.clear()
            return jsonify({
                'status': 'error',
                'message': '用户不存在'
            }), 401
        
        return jsonify({
            'status': 'success',
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 
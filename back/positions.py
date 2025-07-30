from flask import Blueprint, request, jsonify, session
from models import db, Position

# 创建positions蓝图
positions_bp = Blueprint('positions', __name__, url_prefix='/api/positions')

# 获取所有职位
@positions_bp.route('/', methods=['GET', 'OPTIONS'])
def get_positions():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        positions = Position.query.all()
        
        return jsonify({
            'status': 'success',
            'data': [position.to_dict() for position in positions]
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取单个职位
@positions_bp.route('/<int:position_id>', methods=['GET', 'OPTIONS'])
def get_position(position_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        position = Position.query.get(position_id)
        
        if not position:
            return jsonify({
                'status': 'error',
                'message': '职位不存在'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': position.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 创建职位
@positions_bp.route('/', methods=['POST', 'OPTIONS'])
def create_position():
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
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'status': 'error',
                    'message': f'{field} 是必需的'
                }), 400
        
        # 检查职位名称是否已存在
        existing_position = Position.query.filter_by(name=data['name']).first()
        if existing_position:
            return jsonify({
                'status': 'error',
                'message': '职位名称已存在'
            }), 400
        
        new_position = Position(
            name=data['name'],
            description=data['description']
        )
        
        db.session.add(new_position)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '职位创建成功',
            'data': new_position.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 更新职位
@positions_bp.route('/<int:position_id>', methods=['PUT', 'OPTIONS'])
def update_position(position_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        position = Position.query.get(position_id)
        
        if not position:
            return jsonify({
                'status': 'error',
                'message': '职位不存在'
            }), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'name' in data:
            # 检查新名称是否与其他职位冲突
            existing_position = Position.query.filter_by(name=data['name']).first()
            if existing_position and existing_position.id != position_id:
                return jsonify({
                    'status': 'error',
                    'message': '职位名称已存在'
                }), 400
            position.name = data['name']
        
        if 'description' in data:
            position.description = data['description']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '职位信息更新成功',
            'data': position.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 删除职位
@positions_bp.route('/<int:position_id>', methods=['DELETE', 'OPTIONS'])
def delete_position(position_id):
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # 检查用户是否已登录
        if 'user_id' not in session:
            return jsonify({
                'status': 'error',
                'message': '请先登录'
            }), 401
        
        position = Position.query.get(position_id)
        
        if not position:
            return jsonify({
                'status': 'error',
                'message': '职位不存在'
            }), 404
        
        # 检查是否有员工使用此职位（这里需要根据实际业务逻辑调整）
        # from models import Employee
        # employees_with_position = Employee.query.filter_by(position_id=position_id).first()
        # if employees_with_position:
        #     return jsonify({
        #         'status': 'error',
        #         'message': '该职位下还有员工，无法删除'
        #     }), 400
        
        db.session.delete(position)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '职位删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 
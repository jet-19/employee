import requests
import json

# API基础URL
BASE_URL = 'http://localhost:5000'

def test_api():
    """测试登录注册API功能"""
    print("开始测试Flask 用户管理系统API...")
    
    # 测试根路径
    print("\n1. 测试根路径")
    response = requests.get(f'{BASE_URL}/')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试用户注册
    print("\n2. 测试用户注册")
    register_data = {
        'username': 'testuser',
        'password': 'testpass123',
        'role': 'user'
    }
    response = requests.post(
        f'{BASE_URL}/register',
        json=register_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试用户登录
    print("\n3. 测试用户登录")
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = requests.post(
        f'{BASE_URL}/login',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 保存session用于后续测试
    session = requests.Session()
    
    # 测试获取用户信息
    print("\n4. 测试获取用户信息")
    response = session.get(f'{BASE_URL}/profile')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试管理员登录
    print("\n5. 测试管理员登录")
    admin_login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    response = session.post(
        f'{BASE_URL}/login',
        json=admin_login_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试获取所有用户（管理员权限）
    print("\n6. 测试获取所有用户（管理员权限）")
    response = session.get(f'{BASE_URL}/users')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试登出
    print("\n7. 测试用户登出")
    response = session.post(f'{BASE_URL}/logout')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试登出后获取用户信息（应该失败）
    print("\n8. 测试登出后获取用户信息（应该失败）")
    response = session.get(f'{BASE_URL}/profile')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    print("\nAPI测试完成！")

def test_error_cases():
    """测试错误情况"""
    print("\n开始测试错误情况...")
    
    # 测试注册时用户名已存在
    print("\n1. 测试注册时用户名已存在")
    register_data = {
        'username': 'admin',  # 使用已存在的用户名
        'password': 'testpass123'
    }
    response = requests.post(
        f'{BASE_URL}/register',
        json=register_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试登录时密码错误
    print("\n2. 测试登录时密码错误")
    login_data = {
        'username': 'admin',
        'password': 'wrongpassword'
    }
    response = requests.post(
        f'{BASE_URL}/login',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    
    # 测试普通用户访问管理员接口
    print("\n3. 测试普通用户访问管理员接口")
    session = requests.Session()
    
    # 先登录普通用户
    login_data = {
        'username': 'user',
        'password': 'user123'
    }
    response = session.post(
        f'{BASE_URL}/login',
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    # 尝试访问管理员接口
    response = session.get(f'{BASE_URL}/users')
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

if __name__ == '__main__':
    try:
        test_api()
        test_error_cases()
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保Flask应用正在运行")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}") 
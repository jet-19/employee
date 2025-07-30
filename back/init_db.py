import pymysql
from app import app, db, User
from werkzeug.security import generate_password_hash

def init_database():
    """初始化数据库"""
    try:
        # 创建数据库连接
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='password',
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 检查数据库是否存在
        cursor.execute("SHOW DATABASES LIKE 'employee_management'")
        if not cursor.fetchone():
            # 如果数据库不存在，执行init.sql脚本
            print("数据库 'employee_management' 不存在，请先运行 init.sql 脚本")
            return False
        
        cursor.close()
        connection.close()
        
        # 在Flask应用上下文中检查表
        with app.app_context():
            # 检查users表是否存在
            try:
                users = User.query.all()
                print(f"数据库连接成功，当前有 {len(users)} 个用户")
                
                # 检查是否有管理员用户
                admin_user = User.query.filter_by(role='admin').first()
                if not admin_user:
                    # 创建默认管理员用户
                    admin_user = User(
                        username='admin',
                        password=generate_password_hash('admin123'),
                        role='admin'
                    )
                    db.session.add(admin_user)
                    db.session.commit()
                    print("创建默认管理员用户: admin/admin123")
                
                # 检查是否有普通用户
                normal_user = User.query.filter_by(role='user').first()
                if not normal_user:
                    # 创建默认普通用户
                    normal_user = User(
                        username='user',
                        password=generate_password_hash('user123'),
                        role='user'
                    )
                    db.session.add(normal_user)
                    db.session.commit()
                    print("创建默认普通用户: user/user123")
                
                print("数据库初始化完成！")
                
            except Exception as e:
                print(f"数据库表检查失败: {str(e)}")
                return False
            
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("开始初始化数据库...")
    if init_database():
        print("数据库初始化完成！")
        print("\n默认用户账号:")
        print("管理员: admin / admin123")
        print("普通用户: user / user123")
    else:
        print("数据库初始化失败！") 
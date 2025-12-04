from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    # 创建管理员用户
    admin_user = User(username='admin', email='admin@example.com')
    admin_user.set_password('admin123')  # 设置密码
    
    # 创建普通用户
    test_user = User(username='test', email='test@example.com')
    test_user.set_password('123456')  # 设置密码
    
    # 添加到数据库
    db.session.add(admin_user)
    db.session.add(test_user)
    db.session.commit()
    
    print('用户创建成功！')
    print(f'管理员用户: 用户名={admin_user.username}, 密码=admin123')
    print(f'测试用户: 用户名={test_user.username}, 密码=123456')

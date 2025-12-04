from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

app = create_app()
with app.app_context():
    # 获取管理员用户
    admin_user = User.query.filter_by(username='admin').first()
    print(f'管理员用户: {admin_user}')
    
    if admin_user:
        # 测试1: 使用User模型的check_password方法
        print('\n测试1: 使用User模型的check_password方法')
        result1 = admin_user.check_password('admin123')
        print(f'密码验证结果: {result1}')
        
        # 测试2: 直接使用check_password_hash函数
        print('\n测试2: 直接使用check_password_hash函数')
        result2 = check_password_hash(admin_user.password_hash, 'admin123')
        print(f'密码验证结果: {result2}')
        
        # 测试3: 错误密码
        print('\n测试3: 错误密码')
        result3 = admin_user.check_password('wrongpassword')
        print(f'错误密码验证结果: {result3}')
        
        # 查看密码哈希
        print('\n密码哈希:', admin_user.password_hash)

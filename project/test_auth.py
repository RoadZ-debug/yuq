# 直接在应用上下文中测试用户认证功能
from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

# 创建应用实例
app = create_app()

# 在应用上下文中测试
with app.app_context():
    # 获取所有用户
    users = User.query.all()
    print(f"数据库中的用户: {users}")
    
    # 测试特定用户
    admin_user = User.query.filter_by(username='admin').first()
    print(f"\n管理员用户: {admin_user}")
    
    if admin_user:
        print(f"用户名: {admin_user.username}")
        print(f"邮箱: {admin_user.email}")
        print(f"密码哈希: {admin_user.password_hash}")
        
        # 测试密码验证
        password_correct = check_password_hash(admin_user.password_hash, 'admin123')
        print(f"密码验证结果: {password_correct}")
    
    # 测试登录管理器的用户加载
    from app import login_manager
    user_id = admin_user.id if admin_user else 1
    loaded_user = login_manager._user_callback(user_id)
    print(f"\n从ID加载用户: {loaded_user}")

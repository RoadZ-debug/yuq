# 直接测试SystemSetting.get_settings()方法
from app import create_app, db
from app.models import SystemSetting

# 创建应用实例
app = create_app()

# 在应用上下文中测试
with app.app_context():
    print("测试SystemSetting.get_settings()方法...")
    try:
        # 测试获取系统设置
        settings = SystemSetting.get_settings()
        print(f"系统设置对象: {settings}")
        print(f"应用名称: {settings.app_name}")
        print(f"Logo URL: {settings.logo_url}")
        print("\n测试成功!")
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试直接查询
    try:
        settings_query = SystemSetting.query.first()
        print(f"\n直接查询结果: {settings_query}")
    except Exception as e:
        print(f"\n直接查询失败: {e}")
        import traceback
        traceback.print_exc()

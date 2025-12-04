# 重置并重新创建数据库
import os
from app import create_app, db
from app.models import SystemSetting, User, Post, News

# 删除旧数据库文件
if os.path.exists('new_project.db'):
    os.remove('new_project.db')
    print("旧数据库文件已删除")

# 创建应用实例
app = create_app()

# 在应用上下文中重新创建数据库和表
with app.app_context():
    print("正在创建数据库表...")
    
    # 确保所有模型都已导入并注册
    from app.models import SystemSetting, User, Post, News
    
    # 创建所有表
    db.create_all()
    print("数据库表创建完成！")
    
    # 检查所有表是否创建成功
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"已创建的表: {tables}")
    
    # 初始化系统设置
    print("正在初始化系统设置...")
    settings = SystemSetting.get_settings()
    print(f"系统设置初始化完成: {settings}")
    
    # 输出表结构详情
    print("\n表结构详情:")
    for table in tables:
        print(f"\n{table} 表结构:")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  {column['name']} ({column['type']})")
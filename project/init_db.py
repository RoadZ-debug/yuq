# init_db.py

import os
import sqlite3
from app import create_app, db
from app.models import SystemSetting, User, Post, News

# 创建应用实例
app = create_app()

# 在应用上下文中初始化数据库
with app.app_context():
    # 打印数据库路径
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    print(f"数据库路径: {db_path}")
    print(f"数据库文件存在: {os.path.exists(db_path)}")
    
    print("创建数据库表...")
    db.create_all()
    print("数据库表创建完成！")
    
    # 验证表是否存在
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"数据库中的表: {tables}")
    conn.close()
    
    # 尝试获取设置，确保system_setting表中有数据
    print("初始化系统设置...")
    settings = SystemSetting.get_settings()
    print(f"系统设置初始化完成：{settings}")

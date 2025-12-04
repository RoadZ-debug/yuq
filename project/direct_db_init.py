# direct_db_init.py

import os
import sqlite3
from app import create_app
from app import db
import app.models  # 确保所有模型都被导入

# 删除现有的数据库文件（如果存在）
db_path = 'project.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"已删除现有数据库文件: {db_path}")

# 创建应用实例
app = create_app()

# 在应用上下文中初始化数据库
with app.app_context():
    print(f"数据库URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 打印已导入的模型
    print(f"已导入的模型: {db.Model.__subclasses__()}")
    
    # 创建所有表
    print("创建数据库表...")
    db.create_all()
    print("数据库表创建完成！")
    
    # 直接使用SQLite连接验证表是否存在
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"SQLite中的表: {tables}")
    
    # 检查system_setting表结构
    if any(table[0] == 'system_setting' for table in tables):
        cursor.execute("PRAGMA table_info(system_setting);")
        columns = cursor.fetchall()
        print(f"system_setting表结构: {columns}")
    
    conn.close()

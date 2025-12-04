# 直接更新数据库结构脚本
# 用于添加新的数据采集相关表，绕过迁移系统

import os
from app import create_app, db
from app.models import ScrapingTask, TempScrapedNews

# 创建应用实例
app = create_app()

with app.app_context():
    try:
        # 创建所有尚未存在的表
        db.create_all()
        print("数据库表更新成功！")
        print("已创建的表：")
        for table in db.metadata.tables.keys():
            print(f"  - {table}")
    except Exception as e:
        print(f"数据库更新失败：{str(e)}")
        import traceback
        traceback.print_exc()
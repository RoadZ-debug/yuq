# check_db_path.py

import os
from app import create_app

# 创建应用实例
app = create_app()

# 打印详细的配置信息
print(f"数据库URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
print(f"当前工作目录: {os.getcwd()}")
print(f"应用根目录: {app.root_path}")
print(f"应用实例目录: {app.instance_path}")
print(f"DATABASE_URL环境变量: {os.environ.get('DATABASE_URL')}")
print(f"是否存在.env文件: {os.path.exists('.env')}")

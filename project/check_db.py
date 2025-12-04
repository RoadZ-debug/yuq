# 检查Flask应用使用的数据库路径
from app import create_app

app = create_app()
with app.app_context():
    print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    import os
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    print(f"数据库路径: {db_path}")
    print(f"数据库文件存在: {os.path.exists(db_path)}")
    
    # 如果文件存在，检查其中的表
    if os.path.exists(db_path):
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\';')
        tables = [t[0] for t in cursor.fetchall()]
        print(f"数据库中的表: {tables}")
        conn.close()
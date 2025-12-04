# 测试数据库连接和表创建
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# 创建一个简单的Flask应用
app = Flask(__name__)

# 设置数据库路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)

# 定义一个简单的模型
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# 在应用上下文中创建表
with app.app_context():
    # 删除旧表（如果存在）
    db.drop_all()
    # 创建新表
    db.create_all()
    print("表创建完成！")
    
    # 检查表是否存在
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"数据库中的表: {tables}")
    
    # 插入一条测试数据
    test = TestModel(name="测试数据")
    db.session.add(test)
    db.session.commit()
    print("测试数据插入成功！")
    
    # 查询数据
    result = TestModel.query.all()
    print(f"查询结果: {result}")
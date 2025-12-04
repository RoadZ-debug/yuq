# minimal_db_init.py

import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 创建数据库引擎
engine = create_engine('sqlite:///project.db')

# 创建基类
Base = declarative_base()

# 定义模型
class SystemSetting(Base):
    __tablename__ = 'system_setting'
    id = Column(Integer, primary_key=True)
    app_name = Column(String(128), default='政企智能舆情分析报告生成智能体应用系统')
    logo_url = Column(String(256), default='')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    email = Column(String(120))
    password_hash = Column(String(128))
    role = Column(String(16), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(140))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer)

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(64))
    title = Column(String(256))
    summary = Column(Text)
    cover = Column(String(512))
    url = Column(String(512))
    source = Column(String(128))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 创建所有表
print("创建数据库表...")
Base.metadata.create_all(engine)
print("数据库表创建完成！")

# 验证表是否存在
conn = sqlite3.connect('project.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"SQLite中的表: {tables}")
conn.close()

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 初始化系统设置
print("初始化系统设置...")
settings = SystemSetting.query.first()
if not settings:
    settings = SystemSetting()
    session.add(settings)
    session.commit()
print(f"系统设置初始化完成：{settings}")

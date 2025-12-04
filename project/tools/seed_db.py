#!/usr/bin/env python3
# tools/seed_db.py

"""
数据库种子脚本
用于初始化数据库并添加测试数据
"""

import os
import sys
import click
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Post


def seed_database():
    """种子数据库"""
    app = create_app()
    
    with app.app_context():
        print("正在删除现有数据库...")
        db.drop_all()
        
        print("正在创建数据库表...")
        db.create_all()
        
        print("正在创建测试用户...")
        # 创建管理员用户
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 创建普通用户
        user1 = User(username='user1', email='user1@example.com')
        user1.set_password('user123')
        db.session.add(user1)
        
        user2 = User(username='user2', email='user2@example.com')
        user2.set_password('user123')
        db.session.add(user2)
        
        db.session.commit()
        
        print("正在创建测试文章...")
        # 创建测试文章
        post1 = Post(
            title='欢迎使用我们的项目',
            content='这是第一篇测试文章，用于演示项目功能。',
            author=admin
        )
        db.session.add(post1)
        
        post2 = Post(
            title='项目更新说明',
            content='我们已经更新了项目的多个功能，包括用户认证和内容管理。',
            author=user1
        )
        db.session.add(post2)
        
        post3 = Post(
            title='使用指南',
            content='请参考文档了解如何使用这个项目。',
            author=user2
        )
        db.session.add(post3)
        
        db.session.commit()
        
        print("数据库种子创建完成！")
        print(f"创建了 {User.query.count()} 个用户")
        print(f"创建了 {Post.query.count()} 篇文章")


if __name__ == '__main__':
    seed_database()

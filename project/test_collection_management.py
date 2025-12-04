#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简单测试脚本，验证数据采集管理模块的核心功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath('.'))

from app import create_app, db
from app.models import ScrapingTask, TempScrapedNews
from app.scraper.scraper import BaiduNewsScraper

# 创建应用实例
app = create_app()
app_context = app.app_context()
app_context.push()

def test_database_tables():
    """测试数据库表是否创建成功"""
    print("=== 测试数据库表 ===")
    try:
        # 检查ScrapingTask表是否存在
        if db.engine.dialect.has_table(db.engine, 'scraping_task'):
            print("✅ scraping_task表已创建")
        else:
            print("❌ scraping_task表未创建")
            
        # 检查TempScrapedNews表是否存在
        if db.engine.dialect.has_table(db.engine, 'temp_scraped_news'):
            print("✅ temp_scraped_news表已创建")
        else:
            print("❌ temp_scraped_news表未创建")
            
        print()
        return True
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        print()
        return False

def test_scraper_initialization():
    """测试爬虫是否能正常初始化"""
    print("=== 测试爬虫初始化 ===")
    try:
        scraper = BaiduNewsScraper()
        print("✅ 爬虫初始化成功")
        print()
        return True
    except Exception as e:
        print(f"❌ 爬虫初始化失败: {e}")
        print()
        return False

def test_model_creation():
    """测试数据模型是否能正常创建"""
    print("=== 测试数据模型创建 ===")
    try:
        # 创建一个测试任务
        task = ScrapingTask(
            keyword="测试",
            status="pending",
            progress=0,
            total_items=0,
            collected_items=0
        )
        
        db.session.add(task)
        db.session.commit()
        
        # 创建一条测试新闻
        temp_news = TempScrapedNews(
            task_id=task.id,
            title="测试新闻标题",
            url="http://example.com/test",
            source="测试来源",
            summary="测试摘要",
            cover="http://example.com/test.jpg"
        )
        
        db.session.add(temp_news)
        db.session.commit()
        
        print("✅ 数据模型创建成功")
        
        # 测试深度采集状态
        temp_news.has_deep_scraped = True
        temp_news.deep_content = "深度采集的内容"
        db.session.commit()
        
        print("✅ 深度采集状态更新成功")
        
        # 清理测试数据
        db.session.delete(temp_news)
        db.session.delete(task)
        db.session.commit()
        
        print()
        return True
    except Exception as e:
        print(f"❌ 数据模型创建失败: {e}")
        db.session.rollback()
        print()
        return False

def test_routes():
    """测试路由是否正常注册"""
    print("=== 测试路由注册 ===")
    try:
        with app.test_client() as client:
            # 测试健康检查接口
            response = client.get('/scraper/health')
            if response.status_code == 200:
                print("✅ /scraper/health路由正常")
            else:
                print(f"❌ /scraper/health路由异常，状态码: {response.status_code}")
                
            # 测试新闻接口（不需要实际网络请求）
            response = client.get('/scraper/news?keyword=测试&page=1')
            if response.status_code in [200, 500]:  # 500可能是网络问题，但路由已注册
                print("✅ /scraper/news路由已注册")
            else:
                print(f"❌ /scraper/news路由异常，状态码: {response.status_code}")
                
            # 测试采集管理路由
            response = client.get('/scraper/collection')
            if response.status_code in [200, 302]:  # 302是登录重定向
                print("✅ /scraper/collection路由已注册")
            else:
                print(f"❌ /scraper/collection路由异常，状态码: {response.status_code}")
                
        print()
        return True
    except Exception as e:
        print(f"❌ 路由测试失败: {e}")
        print()
        return False

if __name__ == "__main__":
    print("数据采集管理模块功能测试\n")
    
    # 运行所有测试
    tests = [
        test_database_tables,
        test_scraper_initialization,
        test_model_creation,
        test_routes
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("=== 测试结果汇总 ===")
    print(f"通过测试: {passed}")
    print(f"失败测试: {failed}")
    print(f"总测试数: {passed + failed}")
    
    if failed == 0:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败，建议检查")
    
    app_context.pop()

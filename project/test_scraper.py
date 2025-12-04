#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试数据抓取模块功能
"""

import requests
import json

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    url = "http://127.0.0.1:5000/scraper/health"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data["success"]:
            print("✅ 健康检查接口正常")
            print(f"   响应: {data}")
        else:
            print("❌ 健康检查接口异常")
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {data}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    print()

def test_news_scraper(keyword="科技"):
    """测试新闻抓取接口"""
    print(f"=== 测试新闻抓取接口 (关键字: {keyword}) ===")
    url = f"http://127.0.0.1:5000/scraper/news?keyword={keyword}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data["success"]:
            print(f"✅ 新闻抓取成功")
            print(f"   共抓取到 {data['total']} 条新闻")
            
            # 打印前3条新闻的简要信息
            if data['total'] > 0:
                print("\n   前3条新闻信息:")
                for i, news in enumerate(data['data'][:3], 1):
                    print(f"   {i}. 标题: {news['title']}")
                    print(f"      来源: {news['source']}")
                    print(f"      URL: {news['url']}")
                    print(f"      摘要: {news['summary'][:100]}...")
                    print()
        else:
            print("❌ 新闻抓取失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {data.get('message', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    print()

def test_invalid_keyword():
    """测试无效关键字的处理"""
    print("=== 测试无效关键字处理 ===")
    url = "http://127.0.0.1:5000/scraper/news"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 400 and not data["success"]:
            print("✅ 无效关键字处理正确")
            print(f"   错误信息: {data['message']}")
        else:
            print("❌ 无效关键字处理异常")
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {data}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    print()

if __name__ == "__main__":
    print("数据抓取模块功能测试\n")
    
    # 测试健康检查接口
    test_health_check()
    
    # 测试无效关键字处理
    test_invalid_keyword()
    
    # 测试不同关键字的抓取
    test_news_scraper("科技")
    test_news_scraper("经济")
    
    print("=== 测试完成 ===")

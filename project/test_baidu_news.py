#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试百度新闻页面结构 - 详细版本
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import brotli

def test_baidu_news(keyword="科技"):
    """测试百度新闻页面结构 - 详细版本"""
    # 定义百度新闻搜索URL和参数
    base_url = "https://www.baidu.com/s"
    params = {
        "rtt": "1",  # 实时排序
        "bsst": "1",
        "cl": "2",  # 新闻类型
        "tn": "news",
        "rsv_dl": "ns_pc",
        "word": keyword,  # 让requests自动处理URL编码
        "pn": 0  # 第一页
    }

    # 定义请求头
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "connection": "keep-alive",
        "host": "www.baidu.com",
        "referer": "https://news.baidu.com/",
        "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
    }

    try:
        print(f"\n开始获取百度新闻页面（关键字: {keyword}）...")
        
        # 发送请求
        response = requests.get(
            base_url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # 检查请求是否成功
        
        print(f"✅ 请求成功，状态码: {response.status_code}")
        print(f"✅ 内容类型: {response.headers.get('content-type')}")
        print(f"✅ 原始编码: {response.encoding}")
        
        # 处理压缩内容
        content = response.text
        
        print(f"✅ 通过response.text成功解析")
        soup = BeautifulSoup(content, 'html.parser')
        print(f"✅ 页面标题: {soup.title.text if soup.title else '无'}")
        print(f"✅ 内容长度: {len(content)} 字符")
        
        # 检测页面是否包含百度相关内容
        if "百度" in content:
            print("✅ 页面包含百度相关内容")
        else:
            print("❌ 页面可能被拦截或重定向")
    
        # 保存完整页面到文件以便详细检查
        with open("baidu_news.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("📄 完整页面已保存到baidu_news.html")
        
        # 尝试解析新闻列表
        print("\n开始解析新闻列表...")
        
        # 检查content_left容器
        content_left = soup.find("div", id="content_left")
        if content_left:
            print(f"✅ 找到content_left容器，包含 {len(content_left.find_all('div'))} 个div元素")
            
            # 保存content_left的内容到文件以便检查
            with open("baidu_news_content_left.html", "w", encoding="utf-8") as f:
                f.write(str(content_left))
            print("✅ content_left内容已保存到baidu_news_content_left.html")
            
            # 详细检查content_left中的所有元素
            print("\ncontent_left中的元素结构:")
            for child in content_left.children:
                if child.name:
                    print(f"  - {child.name} (class: {child.get('class')}, id: {child.get('id')})")
                    # 如果是div且有子元素，继续检查
                    if child.name == 'div' and child.children:
                        for grandchild in child.children:
                            if grandchild.name:
                                print(f"    + {grandchild.name} (class: {grandchild.get('class')}, id: {grandchild.get('id')})")
        else:
            print("❌ 未找到content_left容器")
            # 检查body下的所有div
            body_divs = soup.body.find_all('div') if soup.body else []
            print(f"🔍 body下共有 {len(body_divs)} 个div元素")
            # 打印前10个div的信息
            for i, div in enumerate(body_divs[:10]):
                print(f"  Div {i}: id={div.get('id')}, class={div.get('class')}")
        
        # 检查是否有新闻条目
        print("\n尝试不同的选择器查找新闻条目:")
        
        # 选择器1: .result-op.c-container
        news_items1 = soup.select(".result-op.c-container")
        print(f"1. .result-op.c-container: {len(news_items1)} 个结果")
        
        # 选择器2: .c-container
        news_items2 = soup.select(".c-container")
        print(f"2. .c-container: {len(news_items2)} 个结果")
        
        # 选择器3: .news-item
        news_items3 = soup.select(".news-item")
        print(f"3. .news-item: {len(news_items3)} 个结果")
        
        # 选择器4: 所有包含h3的div
        news_items4 = [div for div in soup.find_all('div') if div.find('h3')]
        print(f"4. 包含h3的div: {len(news_items4)} 个结果")
        
        # 如果找到包含h3的div，打印前3个的结构
        if news_items4:
            print("\n前3个包含h3的div结构:")
            for i, div in enumerate(news_items4[:3]):
                print(f"\n新闻条目 {i+1}:")
                print(f"  - div class: {div.get('class')}")
                print(f"  - div id: {div.get('id')}")
                print(f"  - 标题: {div.find('h3').text.strip() if div.find('h3') else '无'}")
                a_tag = div.find('h3').find('a') if div.find('h3') else None
                if a_tag:
                    print(f"  - URL: {a_tag.get('href')}")
                
                # 查找来源信息
                source_spans = div.find_all('span')
                for span in source_spans:
                    if span.text.strip() and len(span.text.strip()) < 20:
                        print(f"  - 来源: {span.text.strip()}")
                
                # 查找摘要
                divs = div.find_all('div')
                for d in divs:
                    if d.text.strip() and len(d.text.strip()) > 50 and len(d.text.strip()) < 200:
                        print(f"  - 摘要: {d.text.strip()}")
        
        # 查找页面中的所有h3标签（通常新闻标题用h3）
        h3_tags = soup.find_all('h3')
        print(f"\n页面中共有 {len(h3_tags)} 个h3标签")
        if h3_tags:
            print("前5个h3标签的内容:")
            for i, h3 in enumerate(h3_tags[:5]):
                print(f"  {i+1}. {h3.text.strip()}")
                a_tag = h3.find('a')
                if a_tag:
                    print(f"     URL: {a_tag.get('href')}")

    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("测试百度新闻页面结构 - 详细版本\n")
    test_baidu_news("科技")

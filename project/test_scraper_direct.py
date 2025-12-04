# 直接测试scraper模块的抓取和解析功能
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 模拟scraper的抓取和解析过程
print("直接测试百度新闻抓取和解析...")

# 使用与scraper相同的参数和请求头
base_url = "https://www.baidu.com/s"
params = {
    "rtt": "1",  # 实时排序
    "bsst": "1",
    "cl": "2",  # 新闻类型
    "tn": "news",
    "rsv_dl": "ns_pc",
    "word": "科技",  # 直接使用关键字，让requests自动处理URL编码
    "pn": 0  # 第一页
}

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
    # 发送请求
    response = requests.get(base_url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    print(f"✅ 请求成功，状态码: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"✅ 页面标题: {soup.title.text if soup.title else '无'}")
    
    # 保存完整页面
    with open("scraper_debug_full.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    # 解析页面
    content_left = soup.find("div", id="content_left")
    if content_left:
        print(f"✅ 找到content_left容器")
        
        # 保存content_left
        with open("scraper_debug_content_left.html", "w", encoding="utf-8") as f:
            f.write(str(content_left))
        
        # 尝试不同的选择器
        print("\n选择器测试结果：")
        
        # 选择器1: .news-item
        news_items1 = content_left.select(".news-item")
        print(f"1. .news-item: {len(news_items1)} 个结果")
        
        # 选择器2: .result-op.c-container
        news_items2 = content_left.select(".result-op.c-container")
        print(f"2. .result-op.c-container: {len(news_items2)} 个结果")
        
        # 选择器3: .c-container
        news_items3 = content_left.select(".c-container")
        print(f"3. .c-container: {len(news_items3)} 个结果")
        
        # 选择器4: 所有包含h3的div
        news_items4 = [div for div in content_left.find_all('div') if div.find('h3')]
        print(f"4. 包含h3的div: {len(news_items4)} 个结果")
        
        # 如果找到包含h3的div，尝试解析新闻
        if news_items4:
            print(f"\n尝试解析 {len(news_items4)} 个新闻条目...")
            
            news_list = []
            seen_titles = set()
            seen_urls = set()
            
            for i, item in enumerate(news_items4[:5]):  # 只解析前5个
                try:
                    # 提取标题和链接
                    title_elem = item.find("h3")
                    if not title_elem:
                        continue
                    
                    a_tag = title_elem.find("a")
                    if not a_tag:
                        continue
                    
                    title = a_tag.text.strip()
                    url = a_tag.get("href", "")
                    
                    if not title or not url:
                        continue
                    
                    if title in seen_titles or url in seen_urls:
                        continue
                    
                    seen_titles.add(title)
                    seen_urls.add(url)
                    
                    # 提取来源
                    source_elem = item.find("span", class_="c-gray")
                    if not source_elem:
                        source_elem = item.find("span", class_="c-color-gray")
                    source = source_elem.text.strip() if source_elem else "未知来源"
                    
                    # 提取摘要
                    summary_elem = item.find("div", class_="c-font-normal")
                    if not summary_elem:
                        summary_elem = item.find("div", class_="c-summary")
                    summary = summary_elem.text.strip() if summary_elem else ""
                    
                    # 提取封面图片
                    cover = ""
                    img_elem = item.find("img")
                    if img_elem:
                        cover = img_elem.get("src", "")
                        if cover and not cover.startswith("http"):
                            cover = "https://www.baidu.com" + cover
                    
                    # 添加到新闻列表
                    news_item = {
                        "title": title,
                        "url": url,
                        "source": source,
                        "summary": summary,
                        "cover": cover
                    }
                    news_list.append(news_item)
                    
                    print(f"\n新闻条目 {i+1}:")
                    print(f"  标题: {title}")
                    print(f"  URL: {url}")
                    print(f"  来源: {source}")
                    print(f"  摘要: {summary[:100]}..." if summary else "  摘要: 无")
                    print(f"  封面: {cover}")
                    
                except Exception as e:
                    print(f"解析新闻条目 {i+1} 失败: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            print(f"\n成功解析 {len(news_list)} 条新闻")
        
        # 查看content_left的前1000个字符
        print("\ncontent_left前1000个字符：")
        content_left_str = str(content_left)
        print(content_left_str[:1000])
        
        # 检查是否有特殊的class或id
        print("\ncontent_left中的div元素class和id：")
        for i, div in enumerate(content_left.find_all('div')[:10]):
            print(f"  Div {i}: class={div.get('class')}, id={div.get('id')}")
    else:
        print("❌ 未找到content_left容器")
        print(f"页面内容长度: {len(response.text)} 字符")
        print(f"页面前500字符: {response.text[:500]}")
        
        # 检查是否有其他可能的容器
        all_divs = soup.find_all('div')[:10]
        print("\n页面前10个div：")
        for i, div in enumerate(all_divs):
            print(f"  Div {i}: id={div.get('id')}, class={div.get('class')}")
            
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

# 如果没有抓取到新闻，保存页面内容以便调试
try:
    if not news_list:
        print("\n调试信息：")
        import requests
        from bs4 import BeautifulSoup
        
        # 使用与scraper相同的参数和请求头
        base_url = "https://www.baidu.com/s"
        params = {
            "rtt": "1",  # 实时排序
            "bsst": "1",
            "cl": "2",  # 新闻类型
            "tn": "news",
            "rsv_dl": "ns_pc",
            "word": "科技",
            "pn": 0
        }
        
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
        
        # 发送请求
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 保存页面内容
        with open("scraper_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # 检查页面结构
        content_left = soup.find("div", id="content_left")
        if content_left:
            print(f"✅ 找到content_left容器")
            print(f"   包含 {len(content_left.find_all('div'))} 个div元素")
            
            # 检查各种选择器
            print("\n调试选择器结果：")
            print(f"1. .news-item: {len(content_left.select('.news-item'))} 个结果")
            print(f"2. .result-op.c-container: {len(content_left.select('.result-op.c-container'))} 个结果")
            print(f"3. .c-container: {len(content_left.select('.c-container'))} 个结果")
            print(f"4. 包含h3的div: {len([div for div in content_left.find_all('div') if div.find('h3')])} 个结果")
            
            # 查看content_left的前500个字符
            print("\ncontent_left前500个字符：")
            print(str(content_left)[:500])
        else:
            print("❌ 未找到content_left容器")
            print(f"页面标题: {soup.title.text if soup.title else '无'}")
except NameError:
    print("⚠️  未定义news_list变量")

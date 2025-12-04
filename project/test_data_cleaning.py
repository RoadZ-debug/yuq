# 测试数据清洗过滤功能
import requests

print("=== 测试数据清洗过滤功能 ===")

# 1. 测试数据抓取API，使用普通关键字
print("\n1. 使用普通关键字测试数据抓取:")
keyword = "科技"
page = 1
api_url = f'http://localhost:5000/scraper/news?keyword={keyword}&page={page}'
response = requests.get(api_url)
print(f"   API URL: {api_url}")
print(f"   状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   API响应: 成功={data['success']}, 消息={data['message']}, 总数={data['total']}")
    
    if data['success'] and data['total'] > 0:
        # 打印部分新闻数据，检查字段完整性
        print(f"\n   返回的新闻数据示例:")
        for i, news in enumerate(data['data'][:3]):
            print(f"\n   新闻{i+1}:")
            print(f"      标题: {news['title']}")
            print(f"      URL: {news['url']}")
            print(f"      来源: {news['source']}")
            print(f"      摘要: {news['summary'][:50]}..." if news['summary'] else "      摘要: (空)")
            print(f"      封面: {'有' if news['cover'] else '无'}")

# 2. 检查服务器日志，查看是否有脏数据被过滤的记录
print("\n2. 检查服务器日志，查看脏数据过滤情况:")
print("   (请在服务器运行终端查看详细日志)")

# 3. 测试边界情况
print("\n3. 测试边界情况 (可能产生较多脏数据的关键字):")
keyword = "　"  # 使用空白字符作为关键字
api_url = f'http://localhost:5000/scraper/news?keyword={keyword}&page={page}'
response = requests.get(api_url)
print(f"   API URL: {api_url}")
print(f"   状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   API响应: 成功={data['success']}, 消息={data['message']}, 总数={data['total']}")

print("\n=== 测试完成 ===")

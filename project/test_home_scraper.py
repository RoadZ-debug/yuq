# 测试首页数据抓取功能
import requests

print("=== 测试首页数据抓取功能 ===")

# 1. 访问首页
print("\n1. 访问首页:")
response = requests.get('http://localhost:5000/')
print(f"   状态码: {response.status_code}")
print(f"   页面标题: {response.text.split('<title>')[1].split('</title>')[0] if '<title>' in response.text else '未找到'}")
print(f"   是否包含新闻搜索表单: {'news-search-form' in response.text}")
print(f"   是否包含登录链接: {'登录' in response.text and 'auth.login' in response.text}")
print(f"   是否包含注册链接: {'注册' in response.text and 'auth.register' in response.text}")

# 2. 直接调用数据抓取API
print("\n2. 测试数据抓取API:")
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
        print(f"   第一条新闻: {data['data'][0]['title']} (来源: {data['data'][0]['source']})")

print("\n=== 测试完成 ===")

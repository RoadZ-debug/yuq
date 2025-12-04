import requests

# 测试登录请求
url = 'http://127.0.0.1:5000/auth/login'

# 发送GET请求获取登录页面
try:
    response = requests.get(url)
    print(f"GET请求状态码: {response.status_code}")
    print(f"GET请求响应内容: {response.text[:500]}...")  # 只打印前500个字符
except Exception as e:
    print(f"GET请求失败: {e}")

# 发送POST请求测试登录
data = {
    'username': 'admin',
    'password': 'admin123'
}

try:
    # 不跟随重定向，获取初始响应
    response = requests.post(url, data=data, allow_redirects=False)
    print(f"\nPOST请求状态码: {response.status_code}")
    print(f"POST请求响应头: {dict(response.headers)}")
    
    # 检查是否有重定向
    if response.status_code in [301, 302, 303, 307, 308]:
        redirect_url = response.headers.get('Location')
        print(f"重定向URL: {redirect_url}")
        
        # 跟随重定向获取最终页面
        if redirect_url.startswith('/'):
            redirect_url = f"http://127.0.0.1:5000{redirect_url}"
        response = requests.get(redirect_url, cookies=response.cookies)
        print(f"\n跟随重定向后的状态码: {response.status_code}")
        print(f"跟随重定向后的响应内容: {response.text[:500]}...")
        
        # 检查是否成功跳转到数据抓取页面
        if '数据抓取' in response.text:
            print("\n✅ 登录成功并成功跳转到数据抓取页面！")
        else:
            print("\n❌ 登录成功但未跳转到数据抓取页面！")
    else:
        print(f"POST请求响应内容: {response.text}")
except Exception as e:
    print(f"\nPOST请求失败: {e}")
    import traceback
    traceback.print_exc()

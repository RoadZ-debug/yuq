# run.py

from app import create_app

# 创建Flask应用实例
app = create_app()

if __name__ == '__main__':
    # 启动Flask开发服务器，指定端口为5000
    app.run(debug=True, port=5000)

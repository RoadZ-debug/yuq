# 项目名称

## 项目概述

这里是项目的简要描述。请说明项目的用途、主要功能和目标用户群体。

## 目录结构

```
project/
 ├── app/              # 主应用代码
 ├── migrations/       # 数据库迁移文件
 ├── tests/            # 测试代码
 ├── static/           # 静态资源文件 (CSS, JS, 图片等)
 ├── templates/        # 模板文件
 ├── docs/             # 文档
 ├── requirements/     # 依赖文件
 ├── tools/            # 工具脚本
 ├── .env              # 环境变量配置
 └── README.md         # 项目说明
```

## 安装说明

### 环境要求

- Python 3.8+
- pip 20.0+
- [可选] 虚拟环境工具（如 venv、virtualenv）

### 安装步骤

1. **克隆项目**

   ```bash
   git clone https://github.com/yourusername/project.git
   cd project
   ```

2. **创建虚拟环境（推荐）**

   ```bash
   # 使用 venv
   python -m venv venv
   
   # 激活虚拟环境
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements/dev.txt
   ```

4. **配置环境变量**

   复制 `.env.example` 文件并重命名为 `.env`，然后根据需要修改配置：

   ```bash
   cp .env.example .env
   # 使用编辑器修改 .env 文件
   ```

5. **初始化数据库**

   ```bash
   # 创建数据库表
   flask db upgrade
   
   # 可选：添加初始数据
   flask seed
   ```

## 使用方法

### 开发模式

```bash
flask run
```

应用将在 `http://localhost:5000` 启动。

### 生产模式

建议使用 WSGI 服务器（如 Gunicorn）运行应用：

```bash
gunicorn -w 4 app:app
```

## 测试

运行测试：

```bash
pytest
```

## 数据抓取模块

### 功能介绍

数据抓取模块用于从百度新闻抓取新闻数据，支持自定义关键字搜索和分页。

### API接口

#### 获取新闻数据

```
GET /scraper/news
```

**参数：**
- `keyword`：搜索关键字（必填）
- `page`：页码（可选，默认1）

**响应示例：**

```json
{
    "success": true,
    "message": "抓取成功",
    "data": [
        {
            "title": "新闻标题",
            "url": "新闻链接",
            "source": "新闻来源",
            "summary": "新闻摘要",
            "cover": "封面图片链接"
        }
    ],
    "total": 1
}
```

#### 健康检查

```
GET /scraper/health
```

**响应示例：**

```json
{
    "success": true,
    "message": "数据抓取模块运行正常"
}
```

### 使用方法

在首页的"新闻搜索"功能中，输入搜索关键字和页码，点击"搜索新闻"按钮即可获取新闻数据。

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请联系：

- 项目维护者：[Your Name](mailto:your.email@example.com)
- GitHub Issues：[https://github.com/yourusername/project/issues](https://github.com/yourusername/project/issues)

# 数据抓取模块路由
# 提供API接口用于接收自定义关键字并返回抓取结果
# 新增数据采集管理功能

from flask import request, jsonify, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from . import scraper_bp
from .scraper import scraper
from app import db
from app.models import ScrapingTask, TempScrapedNews, News
import time
import threading

@scraper_bp.route('/news', methods=['GET'])
def get_news():
    """
    获取新闻数据API
    :param keyword: 搜索关键字（必填）
    :param page: 页码（可选，默认1）
    :return: JSON格式的新闻列表
    """
    # 获取请求参数
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    
    # 验证关键字是否存在
    if not keyword:
        return jsonify({
            "success": False,
            "message": "关键字不能为空",
            "data": []
        }), 400
    
    try:
        # 调用抓取器获取新闻
        news_list = scraper.fetch_news(keyword, page)
        
        # 返回结果
        return jsonify({
            "success": True,
            "message": "抓取成功",
            "data": news_list,
            "total": len(news_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"抓取失败: {str(e)}",
            "data": []
        }), 500

@scraper_bp.route('/health', methods=['GET'])
def health_check():
    """
    健康检查API
    :return: JSON格式的健康状态
    """
    return jsonify({
        "success": True,
        "message": "数据抓取模块运行正常"
    }), 200

@scraper_bp.route('/')
@login_required
def index():
    """
    数据抓取首页
    :return: 数据抓取模板
    """
    return render_template('scraper/index.html')


# 数据采集管理功能路由
@scraper_bp.route('/collection')
@login_required
def collection_management():
    """
    数据采集管理首页
    :return: 数据采集管理模板
    """
    return render_template('scraper/collection.html')


@scraper_bp.route('/collection/start', methods=['POST'])
@login_required
def start_collection():
    """
    开始数据采集
    :return: JSON响应，包含任务ID
    """
    keyword = request.form.get('keyword')
    if not keyword:
        return jsonify({"success": False, "message": "请输入采集关键字"}), 400
    
    # 创建采集任务
    task = ScrapingTask(
        keyword=keyword,
        status='running',
        user_id=current_user.id if current_user.is_authenticated else None
    )
    db.session.add(task)
    db.session.commit()
    
    # 启动异步采集线程
    def collect_data():
        try:
            # 使用现有爬虫功能获取新闻数据
            news_list = scraper.fetch_news(keyword, page=1)
            
            # 更新任务进度
            task.total_items = len(news_list)
            task.progress = 10  # 初始化进度
            db.session.commit()
            
            # 处理每条采集数据
            for i, news_item in enumerate(news_list):
                # 创建临时新闻数据
                temp_news = TempScrapedNews(
                    task_id=task.id,
                    title=news_item.get('title', ''),
                    summary=news_item.get('summary', ''),
                    cover=news_item.get('cover', ''),
                    url=news_item.get('url', ''),
                    source=news_item.get('source', '')
                )
                db.session.add(temp_news)
                
                # 更新进度
                task.progress = 10 + int((i + 1) / len(news_list) * 90)
                task.collected_items = i + 1
                db.session.commit()
                
                # 模拟采集延迟
                time.sleep(0.5)
            
            # 完成采集
            task.status = 'completed'
            task.progress = 100
            db.session.commit()
            
        except Exception as e:
            # 处理采集错误
            task.status = 'failed'
            task.progress = 0
            db.session.commit()
    
    # 启动采集线程
    threading.Thread(target=collect_data).start()
    
    return jsonify({"success": True, "message": "采集任务已启动", "task_id": task.id})


@scraper_bp.route('/collection/progress/<int:task_id>')
@login_required
def get_collection_progress(task_id):
    """
    获取采集任务进度
    :param task_id: 任务ID
    :return: JSON响应，包含任务状态和进度
    """
    task = ScrapingTask.query.get_or_404(task_id)
    return jsonify({
        "success": True,
        "task_id": task.id,
        "status": task.status,
        "progress": task.progress,
        "total_items": task.total_items,
        "collected_items": task.collected_items
    })


@scraper_bp.route('/collection/results/<int:task_id>')
@login_required
def collection_results(task_id):
    """
    查看采集结果
    :param task_id: 任务ID
    :return: 采集结果模板
    """
    task = ScrapingTask.query.get_or_404(task_id)
    temp_news_list = TempScrapedNews.query.filter_by(task_id=task.id).all()
    
    return render_template('scraper/collection_results.html', task=task, news_list=temp_news_list)


@scraper_bp.route('/collection/deep-scrape/<int:news_id>', methods=['POST'])
@login_required
def deep_scrape_news(news_id):
    """
    深度采集新闻内容
    :param news_id: 临时新闻ID
    :return: JSON响应
    """
    temp_news = TempScrapedNews.query.get_or_404(news_id)
    
    try:
        # 这里可以实现深度采集逻辑
        # 目前暂时使用简单的模拟
        deep_content = f"深度采集内容：{temp_news.title}\n" + "这是通过深度采集获取的详细内容..."
        
        # 更新临时新闻数据
        temp_news.deep_content = deep_content
        temp_news.has_deep_scraped = True
        db.session.commit()
        
        return jsonify({"success": True, "message": "深度采集完成"})
    except Exception as e:
        return jsonify({"success": False, "message": f"深度采集失败：{str(e)}"}), 500


@scraper_bp.route('/collection/save/<int:news_id>', methods=['POST'])
@login_required
def save_to_database(news_id):
    """
    将单条采集数据保存到数据库
    :param news_id: 临时新闻ID
    :return: JSON响应
    """
    temp_news = TempScrapedNews.query.get_or_404(news_id)
    
    try:
        # 保存到正式新闻表
        news = News(
            keyword=temp_news.task.keyword,
            title=temp_news.title,
            summary=temp_news.summary,
            cover=temp_news.cover,
            url=temp_news.url,
            source=temp_news.source
        )
        db.session.add(news)
        db.session.commit()
        
        return jsonify({"success": True, "message": "数据已保存到数据库"})
    except Exception as e:
        return jsonify({"success": False, "message": f"保存失败：{str(e)}"}), 500


@scraper_bp.route('/collection/save-batch', methods=['POST'])
@login_required
def save_batch_to_database():
    """
    批量保存采集数据到数据库
    :return: JSON响应
    """
    news_ids = request.form.getlist('news_ids[]')
    if not news_ids:
        return jsonify({"success": False, "message": "请选择要保存的数据"}), 400
    
    try:
        saved_count = 0
        for news_id in news_ids:
            temp_news = TempScrapedNews.query.get(news_id)
            if temp_news:
                # 保存到正式新闻表
                news = News(
                    keyword=temp_news.task.keyword,
                    title=temp_news.title,
                    summary=temp_news.summary,
                    cover=temp_news.cover,
                    url=temp_news.url,
                    source=temp_news.source
                )
                db.session.add(news)
                saved_count += 1
        
        db.session.commit()
        return jsonify({"success": True, "message": f"已成功保存{saved_count}条数据到数据库"})
    except Exception as e:
        return jsonify({"success": False, "message": f"批量保存失败：{str(e)}"}), 500

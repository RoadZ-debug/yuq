# 数据抓取模块
# 用于从百度新闻接口爬取数据

from flask import Blueprint

# 创建蓝图
scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper')

# 导入路由
from . import routes

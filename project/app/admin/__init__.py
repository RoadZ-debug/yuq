# app/admin/__init__.py

from flask import Blueprint

# 创建admin蓝图
bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

# 导入路由
from app.admin import routes

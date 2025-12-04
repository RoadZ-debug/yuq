# app/main/__init__.py

from flask import Blueprint

# 创建main蓝图
bp = Blueprint('main', __name__)

# 导入路由
from app.main import routes

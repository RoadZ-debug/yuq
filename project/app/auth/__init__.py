# app/auth/__init__.py

from flask import Blueprint

# 创建auth蓝图
bp = Blueprint('auth', __name__)

# 导入路由
from app.auth import routes

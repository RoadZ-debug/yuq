# app/main/routes.py

from flask import render_template, redirect, url_for, flash, g
from flask_login import login_required, current_user
from app import db
from app.models import SystemSetting
from app.main import bp

# 上下文处理器，在所有模板中可用
def get_system_settings():
    """获取系统设置"""
    if not hasattr(g, 'system_settings'):
        g.system_settings = SystemSetting.get_settings()
    return g.system_settings

@bp.route('/')
def index():
    """首页路由"""
    return render_template('main/index.html')

@bp.route('/about')
def about():
    """关于页面路由"""
    return render_template('main/about.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """用户仪表盘路由"""
    return render_template('main/dashboard.html')

@bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """管理员控制台路由"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    return render_template('admin/dashboard.html')

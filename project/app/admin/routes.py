# app/admin/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, SystemSetting
from app.admin import bp

@bp.route('/dashboard')
@login_required
def dashboard():
    """管理员仪表盘页面"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    # 获取系统统计信息
    user_count = User.query.count()
    # 可以根据需要添加更多统计信息
    return render_template('admin/dashboard.html', user_count=user_count)

@bp.route('/users')
@login_required
def users():
    """用户管理页面"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """添加用户页面"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        # 检查用户名是否已存在
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('用户名已被使用')
            return redirect(url_for('admin.add_user'))
            
        # 检查邮箱是否已存在
        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('邮箱已被使用')
            return redirect(url_for('admin.add_user'))
            
        # 创建新用户
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('用户添加成功')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html')

@bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """编辑用户页面"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('用户信息更新成功')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', user=user)

@bp.route('/users/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    """删除用户"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('用户已删除')
    return redirect(url_for('admin.users'))

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """系统设置页面"""
    if not current_user.is_admin():
        flash('没有权限访问该页面')
        return redirect(url_for('main.dashboard'))
    from app.models import SystemSetting
    settings = SystemSetting.get_settings()
    if request.method == 'POST':
        settings.app_name = request.form['app_name']
        # 处理LOGO上传
        if 'logo' in request.files and request.files['logo'].filename != '':
            logo = request.files['logo']
            # 保存文件逻辑
            import os
            import uuid
            from app import create_app
            app = create_app()
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            # 确保文件名唯一
            ext = os.path.splitext(logo.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            file_path = os.path.join(upload_folder, filename)
            logo.save(file_path)
            # 删除旧的LOGO文件
            if settings.logo_url and os.path.exists(os.path.join(upload_folder, settings.logo_url)):
                os.remove(os.path.join(upload_folder, settings.logo_url))
            settings.logo_url = filename
        db.session.commit()
        flash('系统设置已更新')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', settings=settings)

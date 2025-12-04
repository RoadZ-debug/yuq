# app/auth/routes.py

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录路由"""
    print(f"current_user.is_authenticated: {current_user.is_authenticated}")
    
    if current_user.is_authenticated:
        print("User is already authenticated, redirecting to main.index")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        print("POST request received")
        print(f"Form data: {request.form}")
        
        try:
            username = request.form['username']
            password = request.form['password']
            print(f"Username: {username}, Password: {password}")
            
            user = User.query.filter_by(username=username).first()
            print(f"User found: {user}")
            
            if user is None:
                print("User not found")
                flash('用户名或密码错误')
                return redirect(url_for('auth.login'))
                
            if not check_password_hash(user.password_hash, password):
                print("Password incorrect")
                flash('用户名或密码错误')
                return redirect(url_for('auth.login'))
                
            print("Login successful, logging in user")
            remember = request.form.get('remember_me')
            print(f"Remember me: {remember} (type: {type(remember)})")
            # 将remember转换为布尔值
            remember_bool = remember == 'on'
            print(f"Remember bool: {remember_bool}")
            login_user(user, remember=remember_bool)
            
            print(f"User logged in successfully: {user.username}")
            print(f"User is authenticated: {current_user.is_authenticated}")
            print("Redirecting to scraper.index (数据抓取界面)")
            return redirect(url_for('scraper.index'))
        except Exception as e:
            print(f"Error during login: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    print("GET request, rendering login template")
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """登出路由"""
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册路由"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # 设置默认密码为123456
        password = '123456'
        
        # 检查用户名是否已存在
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('用户名已被使用')
            return redirect(url_for('auth.register'))
            
        # 检查邮箱是否已存在
        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('邮箱已被使用')
            return redirect(url_for('auth.register'))
            
        # 创建新用户
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！默认密码为123456，请登录')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

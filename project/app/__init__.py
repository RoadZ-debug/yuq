# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=None):
    """创建并配置Flask应用"""
    # 使用绝对路径设置模板和静态文件夹
    template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # 设置默认配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(app.instance_path, 'project.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 确保instance目录存在
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # 配置应用
    if config_class is None:
        app.config.from_prefixed_env()
    else:
        # 如果传入的是字典，直接更新配置
        if isinstance(config_class, dict):
            app.config.update(config_class)
        else:
            app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # 上下文处理器：将系统设置和当前年份传递给所有模板
    @app.context_processor
    def inject_system_settings():
        from app.models import SystemSetting
        from datetime import datetime
        return {
            'settings': SystemSetting.get_settings(),
            'current_year': datetime.now().year
        }
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.scraper import scraper_bp
    app.register_blueprint(scraper_bp)
    
    return app

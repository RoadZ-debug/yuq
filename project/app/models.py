# app/models.py

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    """加载用户函数"""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(16), default='user')  # 'user' 或 'admin'
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'

class Post(db.Model):
    """文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Post {self.title}>'

class SystemSetting(db.Model):
    """系统设置模型"""
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(128), default='政企智能舆情分析报告生成智能体应用系统')
    logo_url = db.Column(db.String(256), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        """获取系统设置，若不存在则创建默认设置"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings

class News(db.Model):
    """新闻模型"""
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(64), index=True)  # 搜索关键字
    title = db.Column(db.String(256), index=True)  # 标题
    summary = db.Column(db.Text)  # 概要
    cover = db.Column(db.String(512))  # 封面图片URL
    url = db.Column(db.String(512), index=True)  # 原始URL
    source = db.Column(db.String(128))  # 来源
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def __repr__(self):
        return f'<News {self.title}>'


class ScrapingTask(db.Model):
    """数据采集任务模型"""
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(128), nullable=False)  # 采集关键字或需求
    status = db.Column(db.String(32), default='pending')  # pending, running, completed, failed
    progress = db.Column(db.Integer, default=0)  # 采集进度 0-100
    total_items = db.Column(db.Integer, default=0)  # 总采集条目数
    collected_items = db.Column(db.Integer, default=0)  # 已采集条目数
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 创建任务的用户
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # 关联采集的临时数据（未存储到正式表的数据）
    temp_news = db.relationship('TempScrapedNews', backref='task', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ScrapingTask {self.keyword} - {self.status}>'


class TempScrapedNews(db.Model):
    """临时采集的新闻数据模型（未存储到正式表）"""
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('scraping_task.id'))  # 所属采集任务
    title = db.Column(db.String(256), nullable=False)  # 标题
    summary = db.Column(db.Text)  # 概要
    cover = db.Column(db.String(512))  # 封面图片URL
    url = db.Column(db.String(512), nullable=False)  # 原始URL
    source = db.Column(db.String(128))  # 来源
    has_deep_scraped = db.Column(db.Boolean, default=False)  # 是否已执行深度采集
    deep_content = db.Column(db.Text)  # 深度采集的内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    
    def __repr__(self):
        return f'<TempScrapedNews {self.title}>'

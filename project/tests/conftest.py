# tests/conftest.py

import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope='module')
def app():
    """创建测试应用"""
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    
    yield app

@pytest.fixture(scope='module')
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    """创建测试CLI运行器"""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_test(app):
    """创建测试数据库"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def test_user(db_test):
    """创建测试用户"""
    user = User(username='testuser', email='test@example.com')
    user.set_password('123456')
    db_test.session.add(user)
    db_test.session.commit()
    return user

# tests/test_auth.py

import pytest
from app.models import User


def test_login_route(client):
    """测试登录路由"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert '登录'.encode('utf-8') in response.data


def test_register_route(client):
    """测试注册路由"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert '注册'.encode('utf-8') in response.data


def test_logout_route(client, test_user):
    """测试登出路由"""
    # 登录用户
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': '123456'
    }, follow_redirects=True)
    
    # 登出
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert '登录'.encode('utf-8') in response.data


def test_user_registration(client, db_test):
    """测试用户注册功能"""
    # 发送注册请求（现在使用默认密码123456）
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'new@example.com'
    }, follow_redirects=True)
    
    # 验证注册成功
    assert response.status_code == 200
    assert '注册成功'.encode('utf-8') in response.data
    
    # 验证用户已创建
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.email == 'new@example.com'


def test_user_login(client, test_user):
    """测试用户登录功能"""
    # 发送登录请求（使用默认密码123456）
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': '123456'
    }, follow_redirects=True)
    
    # 验证登录成功
    assert response.status_code == 200
    assert '已经登录'.encode('utf-8') in response.data


def test_invalid_login(client, test_user):
    """测试无效登录"""
    # 发送错误的密码（正确密码是123456）
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    # 验证登录失败
    assert response.status_code == 200
    assert '用户名或密码错误'.encode('utf-8') in response.data

# tests/test_main.py

import pytest
from app.models import User


def test_index_route(client):
    """测试首页路由"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'欢迎' in response.data


def test_about_route(client):
    """测试关于页面路由"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'关于' in response.data


def test_index_authenticated(client, test_user):
    """测试登录用户访问首页"""
    # 登录用户
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    
    # 访问首页
    response = client.get('/')
    assert response.status_code == 200
    assert b'已经登录' in response.data

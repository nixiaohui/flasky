# --coding:utf-8--

from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from .. import db
from ..models import Role, User

from . import register
from forms import LoginForm

@register.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    msg = '欢迎您'
    if request.method == 'POST':
        print form.validate_on_submit() # 当有必填项没有填写的情况下为 False, 否则为 True
        username = form.username.data
        password = form.password.data
        form.username.data = ''
        form.password.data = ''
        user = User.query.filter_by(username=username).first()
        if user is None or user.password == password:
            msg = '登录成功'
        else:
            msg = '用户名或密码错误'
    return render_template('login.html',title=u'登录',form=form, msg=msg)

@register.route('/', methods=['GET', 'POST'])
def index():
    msg = None
    username = None
    if request.method == 'POST':
        msg = '数据已经提交'
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username,password=password,role_id=1)
            db.session.add(user)
            db.session.commit()
            msg += ', 用户注册成功.'
        else:
            msg += ', 用户名重复,请重试.'
    return render_template('register.html',msg=msg,username=username)
# coding:utf-8

from datetime import datetime
from flask import render_template, session, redirect, url_for
from ..models import Role

from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    r = 'Guest'
    role = Role.query.all()
    return render_template('index.html',role=role)
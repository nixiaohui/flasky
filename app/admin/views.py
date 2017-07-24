# coding:utf-8

from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import admin

@admin.route('/', methods=['GET', 'POST'])
def index():
    return render_template('admin.html')
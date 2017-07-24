# coding:utf-8

from flask import Flask, render_template
from config import config
from flask_sqlalchemy import  SQLAlchemy
from flask_bootstrap import Bootstrap

import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding()!=default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # config['default'].init_app(app)
    
    db.init_app(app)
    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .register import register as register_blueprint
    app.register_blueprint(register_blueprint, url_prefix='/register')

    return app
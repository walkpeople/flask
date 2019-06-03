#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    模块的初始化
"""
from flask import Flask,request 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config 
from elasticsearch import Elasticsearch 

login = LoginManager()
login.login_view = 'auth.login'

db = SQLAlchemy()
migrate=Migrate()

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    mail.init_app(app)
    
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']],timeout=30) if app.config['ELASTICSEARCH_URL'] else None
    """
        注册蓝图
    """
    
    # 此处绑定日志记录
    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


    return app

from app import models 

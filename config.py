#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    配置密钥
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(basedir,'app.db')
    # 数据发生变动发送信号给应用
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #错误日志发送給邮箱的配置 

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int( os.environ.get('MAIL_PORT') or 25 )
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None  
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['853023114@qq.com']



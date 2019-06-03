#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    错误处理
"""

from flask import render_template 
from app import db
#from logging.handlers import SMTPHandler,RotatingFileHandler
from app.errors import bp



@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):

    db.session.rollback()
    return render_template('error/500.html'),500

"""
    Error: email to admin 

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None 
        if app.config['MAIL_USERNAME']  or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None 
        if app.config['MAIL_USE_TLS']:
            secure = () 
        mail_handler = SMTPHandler(
                mailhost = (app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
             #   fromaddr = 'no-reply@'+ app.config['MAIL_SERVER'],
                fromaddr = 'xianman125@163.com',
                toaddrs = app.config['ADMINS'],
                subject = 'MicroBlog Failure',
                credentials = auth, secure=secure
                )

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        logging.warning("已经为应用配置 错误发送給管理员（通过邮箱）")


        ##save file with local 

    path = os.path.join(os.getcwd(), 'logs')
    logging.warning('日志存放目录 %s '% str(path))
    if not  os.path.exists(path):
        os.mkdir(path)
    file_handler = RotatingFileHandler(path+'/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
     '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler) 


    # 日志降级
    app.logger.setLevel(logging.INFO)
    app.logger.info('MicroBlog Start')



"""




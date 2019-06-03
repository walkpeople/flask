#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    flask_mail 

"""

from flask import render_template,current_app 
from app.email  import send_email 
import logging 


def send_password_reset_email(user):
    logging.warning(current_app.config['ADMINS'][0])
    token = user.get_reset_password_token()
    send_email('[Microblog]重置密码：',sender=current_app.config['ADMINS'][0],
            recipients = [user.email],
            text_body = render_template('email/reset_password.txt',user=user,token=token),
            html_body = render_template('email/reset_password.html',user=user,token=token)
            )

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""
    表单
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length 
from app.models import User 

"""
    登录表单
"""

class LoginForm(FlaskForm):

    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('登录')

"""
    用户注册表单

"""
class RegistrationForm(FlaskForm):
    
    username = StringField('用户名',validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(),Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')


"""
    重置密码

"""

class  ResetPasswordRequestForm(FlaskForm):

    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('点击发送重置密码邮件')


"""
    修改密码
"""
class ResetPasswordForm(FlaskForm):

    password = PasswordField('新密码:', validators=[DataRequired()])
    password2 = PasswordField('重复密码:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('提交')

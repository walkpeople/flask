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

    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

"""
    用户注册表单

"""
class RegistrationForm(FlaskForm):
    
    username = StringField('user',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')



"""
    用户修改信息
"""

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self,original_names, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.original_names = original_names 
    
    def validate_username(self,username):
        if username.data != self.original_names:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please Use a different name')
            

"""
    发布状态
"""
class PostForm(FlaskForm):
    post = TextAreaField('写点什么好么.....', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""

"""


from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, SubmitField 
from wtforms.validators  import DataRequired, Length 
from app.models import User
from flask import request


"""
    用户修改信息
"""

class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    about_me = TextAreaField('签名', validators=[Length(min=0, max=140)])
    submit = SubmitField('提交')

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


"""
    搜索表单类
"""
class SearchForm(FlaskForm):
    q = StringField('搜索',validators=[DataRequired()])
    

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args 
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False 

        super().__init__(*args, **kwargs)




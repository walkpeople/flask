
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""

"""

from app import db
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login  
from hashlib import md5

class User(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 将密码进行 hash 加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码的正确性
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)
    
    #通过gravatar 生成邮箱对应的唯一头像
    def avatar(self ,size):

        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=wavatar&s={}'.format(digest, size)


    def __repr__(self):

        return '<User {}>'.format(self.username)
    
class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):

        return '<Post> {}'.format(self.body)


# flask_login 回调函数
@login.user_loader
def load_user(id):
    return User.query.get(int(id))




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



followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
    )
"""
    用户表
"""
class User(UserMixin,db.Model):

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
            'User',secondary=followers,
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            backref = db.backref('followers', lazy='dynamic'), lazy='dynamic'
            )

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

    #关注某人
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    #取关某人
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
                followers.c.followed_id == user.id).count() > 0

    #关注文章推荐
    def followed_posts(self):
        
        # 关注的用户
        followed =  Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter                    (followers.c.follower_id == self.id)
        # 自己的动态
        own = Post.query.filter_by(user_id=self.id)
        
        # 取并集
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self):

        return '<User {}>'.format(self.username)
    



class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def author(self):
        user = User.query.filter_by(id=self.user_id).first_or_404()  
        return user.username 

    def __repr__(self):

        return '<Post> {}'.format(self.body)


# flask_login 回调函数
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


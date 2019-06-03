
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
import jwt
from time import time 
from jwt.exceptions import ExpiredSignatureError
from app.search import add_to_index, remove_from_index, query_index
import logging 



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

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password':self.id, 'exp':time()+expires_in},
            app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8') 


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except ExpiredSignatureError as error:
            logging.warning('验证token 失败'+str(error))
            return 
        return User.query.get(id)


    def __repr__(self):

        return '<User {}>'.format(self.username)
    

"""
    全文搜索
"""
class SearchableMixin(object):
    
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=1),0
        
        when = []
        for i in range(len(ids)):
            when.append([ids[i],i])

        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total['value']

    @classmethod
    def before_commit(cls,session):
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj,cls)],
            'update': [obj for obj in session.dirty if isinstance(obj,cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]

        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            add_to_index(cls,__tablename__,obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            add_to_index(cls.__tablename__, obj)

        session._changes = None


    @classmethod 
    def reindex(cls):
        for obj in cls.query:
            logging.warning('add new'+str(obj))
            add_to_index(cls.__tablename__, obj)





class Post(SearchableMixin,db.Model):
    
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    
    def author(self):
        user = User.query.fiter_by(id=self.user_id).first_or_404()  
        return user 

    def __repr__(self):

        return '<Post> {}'.format(self.body)

db.event.listen(db.session, 'before_commit',Post.before_commit)
db.event.listen(db.session, 'after_commit', Post.after_commit)


# flask_login 回调函数
@login.user_loader
def load_user(id):
    return User.query.get(int(id))







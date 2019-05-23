#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 user <user@user-pc>
#
# Distributed under terms of the MIT license.

"""

"""
from app import app, db 
from flask import render_template, flash, redirect,url_for,request
from app.forms import LoginForm
from flask_login import current_user, login_user,logout_user,login_required
from app.models import User 
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
import logging

@app.route('/')
@app.route('/index')
@login_required
def index():

    #前期用以模拟用户 
    # user = {'username':'Miguel'}

    posts = [
        {
            'author' : {'username':'John'},
            'body' : 'Beautiful day in Portland'
        },
        {
            'author' : {'username': 'Susan'} ,
            'body'  : 'The Avengers movie was so cool!'
        },
    
            ]

    return render_template('index.html',title='Home',posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm() 

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html',title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

"""
    注册逻辑
"""
@app.route('/register',methods=['GET','POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


"""
    用户主页
"""
@app.route('/user/<username>')         
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    app.logger.info('==> GET User : %s '%user.username)
    posts = [
            {'author':user,'body':'Test Post #1'},
            {'author':user,'body':'Test Post #1'}
    ]

    return render_template('user.html',user=user,posts=posts)



    
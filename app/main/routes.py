from app.main import bp 
from app.main.forms  import PostForm, EditProfileForm, SearchForm 
from app.models import User,Post
from app import db
from flask_login import login_required, current_user 
from flask_wtf import FlaskForm
import logging 
from flask import flash, render_template, redirect, url_for, request, g,current_app 
from datetime import datetime 
from app.translate import translate 
from langdetect import detect 




@bp.route('/',methods=['GET','POST'])
@bp.route('/index', methods=['GET','POST'])
@login_required
def index():

    #前期用以模拟用户 
    # user = {'username':'Miguel'}
    
    form = PostForm() 
    if form.validate_on_submit():
        language = detect(form.post.data)
        logging.warning(language)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        post = Post(body=form.post.data, author=current_user,language=language)
        db.session.add(post)
        db.session.commit() 
        flash("您的动态已经更新") 
        return redirect(url_for('main.index'))
    #posts = [
    #    {
    #        'author' : {'username':'John'},
    #        'body' : 'Beautiful day in Portland'
    #    },
    #    {
    #        'author' : {'username': 'Susan'} ,
    #        'body'  : 'The Avengers movie was so cool!'
    #    },
    #
    #        ]

    page = request.args.get('page', 1 , type=int)
    posts = current_user.followed_posts().paginate(
            page,current_app.config['POST_PRE_PAGE'],False)
    next_url = url_for('main.index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index',page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html',title='Home',posts=posts.items,form=form, next_url=next_url, prev_url=prev_url)


"""
    用户主页
"""
@bp.route('/user/<username>')         
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
            page, current_app.config['POST_PRE_PAGE'], False )
    next_url = url_for('main.user', username=user.username,page=posts.next_num)if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,page=posts.prev_num)if posts.has_prev else None
    return render_template('user.html',user=user,posts=posts.items,next_url=next_url, prev_url=prev_url)


"""
    在视图函数之前执行

"""
    
@bp.before_request 
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm() 
    g.locale = request.headers['Accept-Language'].split(',')[0].lower()


"""
    修改用户的信息
"""
@bp.route('/edit_profile', methods=['GET','POST'])
@login_required 
def edit_profile():
    form = EditProfileForm(current_user.username) 
    if form.validate_on_submit():
        current_user.username = form.username.data 
        current_user.about_me = form.about_me.data 
        db.session.commit() 
        flash('Your changes have been saved ')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me 

    return render_template('edit_profile.html', title='Edit Profile', form=form)


"""
    用户关注
"""
@bp.route('/follow/<username>')
@login_required 
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('User {} Not Found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}'.format(username))
    return redirect(url_for('main.user',username=username))

"""
    取关
"""
@bp.route('/unfollow/<username>')
@login_required 
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow youself')
        return redirect(url_for('main.user', username))
    current_user.unfollow(user)
    db.session.commit() 
    flash('You are not following {}'.format(username))
    return redirect(url_for('main.user',username=username))
        

@bp.route('/explore')
@login_required 
def explore():
    page = request.args.get('page', 1 , type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page,current_app.config['POST_PRE_PAGE'], False)
    next_url = url_for('main.index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)


"""
    翻译页面    
"""
@bp.route('/translate', methods=['POST'])
@login_required 
def translate_text():
    return translate(request.form['text'])


"""
    搜索视图函数
"""
@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page',1, type=int)
    posts,total = Post.search(g.search_form.q.data, page, current_app.config['POST_PRE_PAGE']) 
    for post in posts:
        logging.warning(post.body)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page+1)if total  > page * current_app.config['POST_PRE_PAGE'] else None 
    
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page-1)if page > 1  else None 
    return render_template('search.html',title='搜索', posts=posts, prev_url=prev_url, next_url=next_url) 



















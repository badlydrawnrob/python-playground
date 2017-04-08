from flask import render_template, url_for, flash, redirect, g
from app import app
from flask_security import login_required, current_user
from .models import User


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
# @login_required
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template(
        'index.html',
        title='Home',
        user=user,
        posts=posts
    )


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User {} not found.'.format(nickname))
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template(
        'user.html',
        user=user,
        posts=posts
    )

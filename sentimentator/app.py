# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect, url_for, make_response

from sentimentator.meta import Message, Status
from sentimentator.database import init, get_random_sentence, get_test_sentence, save_annotation, get_score, get_username, count, get_seen_sentence, reset_user_sentences, reset_user_test_sentences
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from functools import wraps, update_wrapper
from werkzeug.http import http_date
from datetime import datetime
from sentimentator.model import db
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'midnight-sun'


login = LoginManager()
login.init_app(app)
login.login_view = 'login'

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


init(app)


def disable_cache(view):
    @wraps(view)
    def disable_cache(*args, **kwargs):
        resp = make_response(view(*args, **kwargs))
        resp.headers['Last-Modified'] = http_date(datetime.now())
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '-1'
        return resp
    return update_wrapper(disable_cache, view)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

from sentimentator.model import User

@app.route('/')
def index():
    """
    Check if user is authenticated and render index page
    Or login page
    """
    if current_user.is_authenticated:
        user_id = current_user._uid
        return render_template('index.html', score=get_score(user_id), username=get_username(user_id))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """"
    Login page
    If user is already authenticated render index page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(_user=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password...')
            return redirect(url_for('login'))
        login_user(user)
        return render_template('index.html', score=get_score(current_user._uid), username=get_username(current_user._uid))
    return render_template('login.html', title='SIGN IN', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect if already logged in
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already exists
        existing_user = User.query.filter_by(user=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User (form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='REGISTER', form=form)

@app.route('/language')
@login_required
def language():
    """ Language selection page """
    if current_user.is_authenticated:
        user_id = current_user._uid
        return render_template('language.html', score=get_score(user_id), username=get_username(user_id))


@app.route('/annotate/<lang>', methods=['GET', 'POST'])
@disable_cache
@login_required
def annotate(lang):
    """
    Annotation page

    lang -- User selected language

    When annotation page is requested with POST method, there is incoming
    annotation data which needs to be validated and saved to database.

    A sensible use case should not allow invalid input, thus error messages
    are not displayed to user, but logged instead.
    """
    if current_user.is_authenticated:
        user_id = current_user._uid
        sen = get_random_sentence(lang)
        score = get_score(user_id)
        if sen is None:
            flash('There are no sentences for the selected language!')
            return redirect(url_for('language', score=score, username=get_username(user_id)))
        else:
            username = get_username(user_id)
            if request.method == 'POST':
                status = save_annotation(request)
                score += 1
                if status == Status.ERR_COARSE:
                    app.logger.error(Message.INPUT_COARSE)
                elif status == Status.ERR_FINE:
                    app.logger.error(Message.INPUT_FINE)
            else:
                pass
        return render_template('annotate.html', lang=lang, sentence=sen, sentence_id=sen.sid, score=score, username=username)

@app.route('/test-annotate/<lang>', methods=['GET', 'POST'])
@disable_cache
@login_required
def test_annotate(lang):
    """
    Annotation page

    lang -- User selected language

    When annotation page is requested with POST method, there is incoming
    annotation data which needs to be validated and saved to database.

    A sensible use case should not allow invalid input, thus error messages
    are not displayed to user, but logged instead.
    """
    
    if current_user.is_authenticated:
        user_id = current_user._uid
        # Get seen tsids for this user
        seen_tsids = get_seen_sentence(user_id)
        sen = get_test_sentence(lang, user_id, seen_tsids)
        # Get an unseen sentence
        score = get_score(user_id)
        if sen is None:
            flash('There are no sentences for the selected language!')
            return redirect(url_for('language', score=score, username=get_username(user_id)))
        else:
            username = get_username(user_id)
            if request.method == 'POST':
                status = save_annotation(request)
                score += 1
                if status == Status.ERR_COARSE:
                    app.logger.error(Message.INPUT_COARSE)
                elif status == Status.ERR_FINE:
                    app.logger.error(Message.INPUT_FINE)
            else:
                pass
        return render_template('test_annotate.html', lang=lang, sentence=sen, sentence_id=sen.tsid, score=score, username=username)


@app.route('/stats')
def stats():
    if current_user.is_authenticated:
        user_id = current_user._uid
        return render_template('stats.html', score=get_score(user_id), username=get_username(user_id),
                           positive=count(user_id, "%pos%"), negative=count(user_id, "%neg%"),
                           neutral=count(user_id, "%neu%"), anticipation=count(user_id, "%ant%"),
                           joy=count(user_id, "%joy%"), surprise=count(user_id, "%sur%"),
                           trust=count(user_id, "%tru%"), anger=count(user_id, "%ang%"),
                           disgust=count(user_id, "%dis%"), fear=count(user_id, "%fea%"),
                           sadness=count(user_id, "%sad%"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reset_sentences', methods=['GET'])
@login_required
def reset_sentences():
    """
    Route to reset the current user's seen test sentences.
    """
    user_id = current_user._uid  # Get the current user's _uid
    reset_user_sentences(user_id)
    return render_template('index.html', score=get_score(user_id), username=get_username(user_id))

@app.route('/reset_test_sentences', methods=['GET'])
@login_required
def reset_test_sentences():
    """
    Route to reset the current user's seen test sentences.
    """
    user_id = current_user._uid  # Get the current user's _uid
    reset_user_test_sentences(user_id)
    return render_template('index.html', score=get_score(user_id), username=get_username(user_id))
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, session, redirect, url_for

from sentimentator.meta import Message, Status
from sentimentator.database import init, get_random_sentence, save_annotation
from sentimentator.model import Sentence
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.urls import url_parse


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'midnight-sun'


login = LoginManager()
login.init_app(app)
#hashed_password = login.hash_password(the_password)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


init(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('SIGN IN')

from sentimentator.model import User

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='SIGN IN', form=form)


@app.route('/')
#@login_required
def index():
    """ Landing page """
    #if not session.get('logged_in'):
        #return render_template('login.html')
    #else:
    return render_template('index.html')


@app.route('/language')
#@login_required
def language():
    """ Language selection page """
    return render_template('language.html')


@app.route('/annotate/<lang>', methods=['GET', 'POST'])
#@login_required
def annotate(lang):
    """
    Annotation page

    lang -- User selected language

    When annotation page is requested with POST method, there is incoming
    annotation data which needs to be validated and saved to database.

    A sensible use case should not allow invalid input, thus error messages
    are not displayed to user, but logged instead.
    """
    if request.method == 'POST':
        status = save_annotation(request)
        if status == Status.ERR_COARSE:
            app.logger.error(Message.INPUT_COARSE)
        elif status == Status.ERR_FINE:
            app.logger.error(Message.INPUT_FINE)
    sen = get_random_sentence(lang)
    return render_template('annotate.html', lang=lang, sentence=sen, sentence_id=sen.sid)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

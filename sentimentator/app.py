# -*- coding: utf-8 -*-

# Skip button
# username + score display on annotation page

from flask import Flask, render_template, request, flash, redirect, url_for

from sentimentator.meta import Message, Status
from sentimentator.database import init, get_random_sentence, save_annotation, get_score, get_username
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'midnight-sun'


login = LoginManager()
login.init_app(app)
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

@app.route('/')
def index():
    """
    Check if user is authenticated and render index page
    Or login page
    """
    if current_user.is_authenticated:
        return render_template('index.html', score=get_score(), username=get_username())
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
        return render_template('index.html', score=get_score(), username=get_username())
    return render_template('login.html', title='SIGN IN', form=form)


@app.route('/language')
@login_required
def language():
    """ Language selection page """
    return render_template('language.html', score=get_score(), username=get_username())


@app.route('/annotate/<lang>', methods=['GET', 'POST'])
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
    sen = get_random_sentence(lang)
    score = get_score()
    if sen is None:
        flash('There are no sentences for the selected language!')
        return redirect(url_for('language', score=score, username=get_username()))
    else:
        username = get_username()
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

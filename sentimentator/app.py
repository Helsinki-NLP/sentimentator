# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

from sentimentator.meta import Message, Status
from sentimentator.database import init, get_random_sentence, save_annotation


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init(app)


@app.route('/')
def index():
    """ Landing page """
    return render_template('index.html')


@app.route('/language')
def language():
    """ Language selection page """
    return render_template('language.html')


@app.route('/annotate/<lang>', methods=['GET', 'POST'])
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
    return render_template('annotate.html', lang=lang, sentence=sen)


@app.route('/logout')
def logout():
    """ Logout page """
    return render_template('logout.html')

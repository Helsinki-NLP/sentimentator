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
    return render_template('index.html')


@app.route('/language')
def language():
    return render_template('language.html')


@app.route('/annotate/<lang>', methods=['GET', 'POST'])
def annotate(lang):
    if request.method == 'POST':
        status = save_annotation(request)
        if status == Status.ERR_COARSE:
            app.logger.error(Message.INPUT_COARSE)
        elif status == Status.ERR_FINE:
            app.logger.error(Message.INPUT_FINE)
    s = get_random_sentence(lang)
    return render_template('annotate.html', lang=lang, sentence=s)


@app.route('/logout')
def logout():
    return render_template('logout.html')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from sqlalchemy.sql.expression import func
#from wtforms import Form, BooleanField, StringField, validators

from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///senti.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/language')
def language():
    return render_template('language.html')

@app.route('/annotate/<lang>', methods=['GET', 'POST'])
def annotate(lang):
    def valid(input):
        valid_fine_sentiments = ['ant', 'joy', 'sur', 'ang', 'fea', 'dis', 'tru', 'sad']
        return input in valid_fine_sentiments

    result = Language.query.filter_by(language=lang).first_or_404()
    random_sentence = Sentence.query \
        .filter_by(language_id=result.id).order_by(func.random()).first()

    coarse = request.form.get('sentiment')
    fine = request.form.getlist('fine-sentiment')
    if request.method == 'POST':
        if coarse == 'neu':
            valid = True
            print('User selected neu')
            tag = Tag(pnn=coarse)
            db.session.add(tag)
            db.session.commit()
        elif coarse in ['pos', 'neg']:
            print('User selected pos or neg')
            if all([valid(x) for x in fine]):
                valid = True
                tag = Tag(pnn=coarse)

                db.session.add(tag)
                db.session.commit()


    return render_template('annotate.html', lang=lang, sentence=random_sentence)


@app.route('/logout')
def logout():
    return render_template('logout.html')

#class AnnotationForm(Form):
#    pos = BooleanField('POSITIVE')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

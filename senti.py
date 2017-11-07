from flask import Flask, render_template, request
from models import db, Language, Sentence
from sqlalchemy.sql.expression import func
import random

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

@app.route('/annotate')
def annotate():
    lang = request.args.get('lang')
    result = Language.query.filter_by(language=lang).first_or_404()
    #print(type(Language.query.all()))
    random_sentence = Sentence.query.with_entities(Sentence.sentence)\
        .filter_by(language_id=result.id).order_by(func.random()).first()

    return render_template('annotate.html', sentence=random_sentence)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run()

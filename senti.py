from flask import Flask, render_template, request
from models import db, Language, Sentence, Sentiment
from sqlalchemy.sql.expression import func

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
    if request.method == 'POST':
        #Sentiment(sentiment=request.form['sentiment'])
        print(request.form.get('sentiment'))
        print(request.form.getlist('fine-sentiment'))
    result = Language.query.filter_by(language=lang).first_or_404()
    random_sentence = Sentence.query\
        .filter_by(language_id=result.id).order_by(func.random()).first()

    return render_template('annotate.html', lang=lang, sentence=random_sentence)

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run()

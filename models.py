from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Sentence(db.Model):
    """model for one of your table"""
    __tablename__ = 'sentence'
    # define your model
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String)
    #source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    #document_id = db.Column(db.Integer, db.ForeignKey('document.id'))

    def __str__(self):
        return self.sentence

class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sentiment_id = db.Column(db.Integer, db.ForeignKey('sentiment.id'))
    pnn = db.Column(db.String)

class Sentiment(db.Model):
    __tablename__ = 'sentiment'
    id = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.String, index=True, unique=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    token = db.Column(db.Integer)

class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.Integer)
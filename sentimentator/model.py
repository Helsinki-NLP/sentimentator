# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String)


class Sentence(db.Model):
    __tablename__ = 'sentence'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

    def __str__(self):
        return self.sentence


class Annotation(db.Model):
    __tablename__ = 'annotation'
    id = db.Column(db.Integer, primary_key=True)
    annotation = db.Column(db.String)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))

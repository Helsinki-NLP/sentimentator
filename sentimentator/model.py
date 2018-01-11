# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
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

    def get_id(self):
        return self.id


class Annotation(db.Model):
    __tablename__ = 'annotation'
    id = db.Column(db.Integer, primary_key=True)
    annotation = db.Column(db.String)
    sentence_id = db.Column(db.Integer, db.ForeignKey('sentence.id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    annotation_id = db.Column(db.Integer, db.ForeignKey('annotation.id'))

    def __init__(self, username, password):
        self.username = username
        self.password_hash = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


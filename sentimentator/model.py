# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()


class Language(db.Model):
    __tablename__ = 'language'
    _lid = db.Column('id', db.Integer, primary_key=True)
    _language = db.Column('language', db.String)

    def __init__(self, id, language):
        self._lid = id
        self._language = language


class Sentence(db.Model):
    __tablename__ = 'sentence'
    _sid = db.Column('id', db.Integer, primary_key=True)
    _sentence = db.Column('sentence', db.String)
    _lid = db.Column('language_id', db.Integer, db.ForeignKey('language.id'))

    def __init__(self, sentence, language_id):
        self._sentence = sentence
        self._lid = language_id

    @property
    def sid(self):
        return self._sid

    def __str__(self):
        return self._sentence


class Annotation(db.Model):
    __tablename__ = 'annotation'
    _aid = db.Column('id', db.Integer, primary_key=True)
    _annotation = db.Column(db.String)
    _sid = db.Column('sentence_id', db.Integer, db.ForeignKey('sentence.id'))
    _uid = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))

    def __init__(self, annotation, sentence_id):
        self._annotation = annotation
        self._sid = sentence_id


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    _uid = db.Column('id', db.Integer, primary_key=True)
    _user = db.Column('user', db.String)
    _pass = db.Column('pass', db.String)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, username):
        self._user = username

    def __init__(self, username):
        self._user = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return self._uid

    # def __repr__(self):
    #     return '<User {}>'.format(self._user)

    def set_password(self, password):
        self._pass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._pass, password)


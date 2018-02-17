# -*- coding: utf-8 -*-

from json import dumps

from sentimentator.meta import Status
from sentimentator.model import db, Language, Sentence, Annotation
from flask_login import current_user
from sqlalchemy.types import Unicode
from sqlalchemy import func, and_
import json


VALID_FINE_SENTIMENTS = ['ant', 'joy', 'sur', 'ang', 'fea', 'dis', 'tru', 'sad']


def init(app):
    """ Initiate datamodel """
    db.init_app(app)


def get_user():
    """ Get id of logged-in user """
    if current_user.is_authenticated():
        user_id = current_user._uid
        return user_id


def get_username():
    if current_user.is_authenticated():
        username = current_user.user
        return username


def get_score():
    """ Get annotation score by returning amount of annotations for logged-in user """
    if current_user.is_authenticated():
        user_id = current_user._uid
        number_of_annotations = db.session.query(Annotation).filter_by(_uid=user_id).count()
        return number_of_annotations


def get_positive():
    if current_user.is_authenticated():
        user_id = current_user._uid
        positive = Annotation.query.filter(and_(Annotation._annotation.like("%pos%")) &
                                                       Annotation._uid == user_id).count()
        return positive


def get_negative():
    if current_user.is_authenticated():
        user_id = current_user._uid
        negative = Annotation.query.filter(and_(Annotation._annotation.like("%neg%")) &
                                                       Annotation._uid == user_id).count()
        return negative

def get_neutral():
    if current_user.is_authenticated():
        user_id = current_user._uid
        neutral = Annotation.query.filter(and_(Annotation._annotation.like("%neu%")) &
                                                       Annotation._uid == user_id).count()
        return neutral


def get_anticipation():
    if current_user.is_authenticated():
        user_id = current_user._uid
        anticipation = Annotation.query.filter(and_(Annotation._annotation.like("%ant%")) &
                                                       Annotation._uid == user_id).count()
        return anticipation

def get_anger():
    if current_user.is_authenticated():
        user_id = current_user._uid
        anger = Annotation.query.filter(and_(Annotation._annotation.like("%ang%")) &
                                                       Annotation._uid == user_id).count()
        return anger

def get_disgust():
    if current_user.is_authenticated():
        user_id = current_user._uid
        disgust = Annotation.query.filter(and_(Annotation._annotation.like("%dis%")) &
                                                       Annotation._uid == user_id).count()
        return disgust

def get_fear():
    if current_user.is_authenticated():
        user_id = current_user._uid
        fear = Annotation.query.filter(and_(Annotation._annotation.like("%fea%")) &
                                                       Annotation._uid == user_id).count()
        return fear


def get_joy():
    if current_user.is_authenticated():
        user_id = current_user._uid
        joy = Annotation.query.filter(and_(Annotation._annotation.like("%joy%")) &
                                                       Annotation._uid == user_id).count()
        return joy


def get_sadness():
    if current_user.is_authenticated():
        user_id = current_user._uid
        sadness = Annotation.query.filter(and_(Annotation._annotation.like("%sad%")) &
                                                       Annotation._uid == user_id).count()
        return sadness


def get_surprise():
    if current_user.is_authenticated():
        user_id = current_user._uid
        surprise = Annotation.query.filter(and_(Annotation._annotation.like("%sur%")) &
                                                       Annotation._uid == user_id).count()
        return surprise

def get_trust():
    if current_user.is_authenticated():
        user_id = current_user._uid
        trust = Annotation.query.filter(and_(Annotation._annotation.like("%tru%")) &
                                                       Annotation._uid == user_id).count()
        return trust


def get_random_sentence(lang):
    """ Fetch a random sentence of given language """
    # TODO: Allow user to annotate only previously unseen sentences or sentences with less than 3 annotations
    language = Language.query.filter_by(_language=lang).first()
    if language is None:
        return None
    else:
        sentence = Sentence.query.filter_by(_lid=language._lid).order_by(func.random()).first()
        return sentence


def _is_valid(fine):
    """ Return true if given argument is valid fine sentiment """
    return fine in VALID_FINE_SENTIMENTS


def _save(user_id, sen_id, data, intensity):
    """
    Save validated sentiments to database

    coarse -- Coarse sentiment
    fine   -- A list of fine sentiments
    """
    json = dumps(data)
    annotation = Annotation(user_id=user_id, sentence_id=sen_id, annotation=json, intensity=intensity)
    db.session.add(annotation)
    db.session.commit()


def save_annotation(req):
    """
    Validate given request and save sentiments to database

    req -- HTTP request object with POST data

    Return Status object indicating the result of the validation.
    """

    user_id = get_user()

    sen_id = req.form.get('sentence-id')
    coarse = req.form.get('sentiment')
    fine = req.form.getlist('fine-sentiment')
    intensity = req.form.get('slider')

    annotation = {
        'coarse': coarse
    }

    if coarse == 'neu':
        pass
    elif coarse in ['pos', 'neg']:
        if all([_is_valid(f) for f in fine]):
            annotation['fine'] = fine
        else:
            return Status.ERR_FINE
    else:
        return Status.ERR_COARSE

    _save(user_id, sen_id, annotation, intensity)
    return Status.OK

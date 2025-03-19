# -*- coding: utf-8 -*-

from json import dumps

from sentimentator.meta import Status
from sentimentator.model import db, Language, Sentence, Annotation, TestSentence, UserSeenSentence
from flask_login import current_user
from sqlalchemy import func
from flask import session


VALID_FINE_SENTIMENTS = ['ant', 'joy', 'sur', 'ang', 'fea', 'dis', 'tru', 'sad']


def init(app):
    """ Initiate datamodel """
    db.init_app(app)


def get_user():
    """ Get id of logged-in user """
    if current_user.is_authenticated():
        user_id = current_user._uid
        return user_id


def get_username(user_id):
    username = current_user.user
    return username


def get_score(user_id):
    """ Get annotation score by returning amount of annotations for logged-in user """
    q = db.session.query(Annotation).filter_by(_uid=user_id)
    return q.count()


def count(user_id, likeness):
    """
    Like parsing JSON is so three minutes ago...

    likeness -- A search string (usually having leading and trailing %'s)

    Returns the number of successful matches.
    """
    q = Annotation.query.filter_by(_uid=user_id)\
        .filter(Annotation._annotation.like(likeness))
    return q.count()

def get_seen_sentence(user_id):
    seen_tsids = {s._tsid for s in UserSeenSentence.query.filter_by(_uid=user_id).all()}
    return seen_tsids

def reset_user_test_sentences(user_id):
    UserSeenSentence.query.filter_by(_uid=user_id).delete()
    Annotation.query.filter_by(_uid=user_id).delete()
    db.session.commit()

def get_random_sentence(lang):
    """ Fetch a random sentence of given language """
    # TODO: Allow user to annotate only previously unseen sentences or sentences with less than 3 annotations
    language = Language.query.filter_by(_language=lang).first()
    if language is None:
        return None
    else:
        sentence = Sentence.query.filter_by(_lid=language._lid).order_by(func.random()).first()
        return sentence


def get_test_sentence(lang, user_id, seen_tsids):
    """ Fetch a specific sentence of given language """
    language = Language.query.filter_by(_language=lang).first()
    if language is None:
        return None

    sentence = TestSentence.query.filter_by(_lid=language._lid).filter(~TestSentence._tsid.in_(seen_tsids)).first()
    # Get all sentences for the language, sorted by tsid

    if sentence:
        # Mark as seen
        seen_entry = UserSeenSentence(_uid=user_id, _tsid=sentence._tsid)
        db.session.add(seen_entry)
        db.session.commit()
        return sentence
    else:
        return None

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

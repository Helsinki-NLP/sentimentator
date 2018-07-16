# -*- coding: utf-8 -*-

from json import dumps

from sentimentator.meta import Status
from sentimentator.model import db, Language, Sentence, Annotation
from flask_login import current_user
from sqlalchemy import func


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
    #TODO: save annotation mode and seed sentence values here.
    # Note: add relevant button to interface.
    # Before using this function:
    # 1) Add the expert users to the db (for example using CLI)
    # 2) Add the _mode and _is_seed columns to the db (for example using CLI)
    # 3) Add rank to db
    # For example, see how users are added in the init_db() function in data_import.py.

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

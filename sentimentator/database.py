# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import func
from json import dumps

from sentimentator.meta import Status
from sentimentator.model import db, Language, Sentence, Annotation, User
from flask_login import current_user


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


def get_random_sentence(lang):
    """ Fetch a random sentence of given language """
    language = Language.query.filter_by(_language=lang).first()
    if language is None:
        return None
    else:
        return Sentence.query \
                   .filter_by(_lid=language._lid) \
                   .order_by(func.random()) \
                   .first()


def _is_valid(fine):
    """ Return true if given argument is valid fine sentiment """
    return fine in VALID_FINE_SENTIMENTS


def _save(user_id, sen_id, data):
    """
    Save validated sentiments to database

    coarse -- Coarse sentiment
    fine   -- A list of fine sentiments
    """
    json = dumps(data)
    annotation = Annotation(user_id=user_id, sentence_id=sen_id, annotation=json)
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

    _save(user_id, sen_id, annotation)
    return Status.OK

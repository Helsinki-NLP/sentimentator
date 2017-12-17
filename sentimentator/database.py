# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import func

from sentimentator.meta import Status
from sentimentator.model import db, Language, Sentence, Tag


VALID_FINE_SENTIMENTS = ['ant', 'joy', 'sur', 'ang', 'fea', 'dis', 'tru', 'sad']


def init(app):
    db.init_app(app)


def get_random_sentence(lang):
    la = Language.query.filter_by(language=lang).first()
    return Sentence.query.filter_by(language_id=la.id).order_by(func.random()).first()


def _is_valid(fine):
    return fine in VALID_FINE_SENTIMENTS


def _save_neutral(fine):
    db.session.add(Tag(pnn='neu'))
    db.session.commit()


def _save(coarse, fine=None):
    if fine is None:
        db.session.add(Tag(pnn=coarse))
    else:
        for f in fine:
            db.session.add(Tag(pnn=coarse, sentiment=f))
    db.session.commit()


def save_annotation(req):
    coarse = req.form.get('sentiment')
    fine = req.form.getlist('fine-sentiment')

    if coarse == 'neu':
        _save('neu')
    elif coarse in ['pos', 'neg']:
        if all([_is_valid(f) for f in fine]):
            _save(coarse, fine)
        else:
            return Status.ERR_FINE
    else:
        return Status.ERR_COARSE

    return Status.OK

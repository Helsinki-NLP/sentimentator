#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sentimentator.app import app
from sentimentator.model import db, Language, Sentence

with open('en.txt') as f:
    en_data = f.readlines()

data = {
    'en': [en_data]
}


with app.app_context():
    db.create_all()
    for i, lang in enumerate(data):
        db.session.add(Language(id=i, language=lang))
        for sentence in data[lang]:
            db.session.add(Sentence(sentence=sentence, language_id=i))
    db.session.commit()
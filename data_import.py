#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sentimentator.app import app
from sentimentator.model import db, Language, Sentence, User

lang_en = []

with open('en.txt') as Sentences_en, open('ids.txt') as Ids:
    for s, i in zip(Sentences_en, Ids):
        lang_en.append([s] + i.split())

# example lang_en = [
#   ['sentence', 'en/...', 'fi/...', '1', '1'],
#   [...]
# ]

data = {
    'en': lang_en,
}

with app.app_context():
    db.create_all()
    admin = User(username='admin')
    admin.set_password('pulla')
    db.session.add(admin)
    for i, lang in enumerate(data):
        db.session.add(Language(id=i, language=lang))
        for row in data[lang]:
            # FIXME What should we actually put to database?
            db.session.add(Sentence(
                sentence=row[0],
                language_id=i,
                opus_did=row[1],
                opus_sid=row[3]))
    db.session.commit()

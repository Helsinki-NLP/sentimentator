#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sentimentator.app import app
from sentimentator.model import db, Language, Sentence, User, Alignment, Document
from argparse import ArgumentParser
import re

# Read the sentences, sentence ids and document ids, return list
def read_file(sentences_fn, alignment_fn):
    lang_data = []
    with open(sentences_fn) as Sentences, open(alignment_fn) as Alignments:
        for s, i in zip(Sentences, Alignments):
            lang_data.append([s] + i.split())
    return lang_data


# example lang_data = [
#   ['sentence', 'en/...', 'fi/...', '1', '1'],
#   [...]
# ]

# Create database with dummy admin user
def init_db():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(_user='admin').first()
        if admin is None:
            db.session.add(User(username='admin'))
        else:
            admin.set_password('flyingtiger')
        db.session.commit()

# Function to check if the language exists in database
# If not, add it
def ensure_language(lang):
    with app.app_context():
        language = Language.query.filter_by(_language=lang).first()
        if language is None:
            db.session.add(Language(language=lang))
            db.session.commit()
            return Language.query.filter_by(_language=lang).first().lid
        else:
            return language.lid

# Import pivot language (en) sentences and metadata
def import_pivot(lang, lang_data):
    with app.app_context():
        language_id = ensure_language(lang)
        for i in lang_data:
            db.session.add(Sentence(
                sentence=i[0],
                    language_id=language_id,
                    opus_did=i[1],
                    opus_sid=i[3]))

        db.session.commit()

# Import non-pivot language sentences and metadata
def import_data(lang, lang_data):
    with app.app_context():
        language_id = ensure_language(lang)
        for i in lang_data:
            db.session.add(Sentence(
                sentence=i[0],
                language_id=language_id,
                opus_did=i[2],
                opus_sid=i[4]))

        db.session.commit()


def main():

    import argparse
    parser = ArgumentParser()

    # Validate language code argument
    def check_arg(l, pattern=re.compile(r'^[a-zA-Z]{2}$')):
        if not pattern.match(l):
            raise argparse.ArgumentTypeError('Use a two-character alphabetic language code.')
        return l

    parser.add_argument('LANG', help='', type=check_arg)
    parser.add_argument('SENTENCES', help='')
    parser.add_argument('ALIGNMENTS', help='')
    args = parser.parse_args()
    init_db()
    lang_data = read_file(args.SENTENCES, args.ALIGNMENTS)
    if args.LANG == 'en': # In this case the pivot language is English
        import_pivot(args.LANG, lang_data)
    else:
        import_data(args.LANG, lang_data)


if __name__ == "__main__":
    main()

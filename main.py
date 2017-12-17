#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sentimentator.app import app


def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()

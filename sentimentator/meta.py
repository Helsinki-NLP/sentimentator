# -*- coding: utf-8 -*-

from enum import Enum


class Status(Enum):
    OK         = 0
    ERR_COARSE = 1
    ERR_FINE   = 2


class Message():
    INPUT_COARSE = 'Invalid coarse sentiment'
    INPUT_FINE   = 'Invalid fine sentiment'

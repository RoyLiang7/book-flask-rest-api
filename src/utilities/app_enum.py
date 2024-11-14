from enum import Enum

class BookType(Enum):
    HARD_COVER = 1
    SOFT_COVER = 2
    MAGAZINE = 3
    LETTERS = 4

class TransType(Enum):
    LATE_TRANS: 1
    EARLY_TRANS: 2
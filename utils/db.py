from mongoengine import *
from .config import _DB

connect(host=_DB)

class Sample(Document):
    message = StringField()
    status = StringField()

class Word(Document):
    word = StringField()
    occurrences = IntField()
    spams = IntField()
    hams = IntField()
    spamProb = FloatField()
    hamProb = FloatField()
    spamProbNormalized = FloatField()
    hamProbNormalized = FloatField()
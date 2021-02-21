from mongoengine import *

connect(host='mongodb+srv://Vlad:naivebayes@samples.5hiaz.mongodb.net/test')

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
from mongoengine import *

connect(host='mongodb+srv://Vlad:naivebayes@samples.5hiaz.mongodb.net/test')

class Sample(Document):
    message = StringField()
    status = StringField()
from mongoengine import *

connect('jdcomment')


class Product(Document):
    skuid = LongField(required=True, unique=True)
    score = ListField(IntField(), default=lambda: [0, 0, 0, 0, 0])
    show_count = IntField()
    comment_count = IntField()
    score_type = DictField()
    meta = {
        'indexes': ['skuid']
    }


class Tag(Document):
    content = StringField(max_length=100, unique=True)
    count = IntField()
    meta = {
        'indexes': ['content']
    }


class Custom(Document):
    level = StringField(max_length=20)
    name = StringField()
    province = StringField()


class Comment(Document):
    product = ReferenceField(Product, required=True)
    comment_id = LongField()
    # tags = ListField(ReferenceField(Tag))
    content = StringField()
    score = IntField()
    useful_vote_count = IntField()
    useless_vote_count = IntField()
    custom = ReferenceField(Custom)
    meat = {
        'indexes': ['product', 'comment_id']
    }

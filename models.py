import random

import mongoengine as me
import time


class User(me.Document):
    id = me.IntField(primary_key=True, default=time.time())
    user = me.StringField(required=True, unique=True)
    password = me.StringField(required=True)
    email = me.StringField(required=True, unique=True)


class Email(me.Document):
    id = me.IntField(primary_key=True, default=time.time())
    email = me.StringField(required=True, unique=True)
    code = me.StringField(required=True)


class Publish(me.Document):
    id = me.IntField(primary_key=True, default=time.time_ns())
    title = me.StringField(required=True)
    content = me.StringField(required=True)
    author = me.StringField(required=True)
    create_time = me.StringField(required=True, default=time.strftime('%Y-%m-%d %H:%M', time.localtime()))



class Answer(me.Document):
    id = me.IntField(primary_key=True, default=time.time())
    content = me.StringField(required=True)
    create_time = me.IntField(required=True, default=time.time())
    publish_id = me.IntField(required=True)
    author = me.StringField(required=True)

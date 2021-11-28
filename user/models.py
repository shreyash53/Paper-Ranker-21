from mongoengine.document import Document
from mongoengine.fields import (EmailField, ListField, ReferenceField,
                                StringField, IntField)
from search.models import Paper
from flask_login import UserMixin

class User(Document, UserMixin):
    username = StringField(required=True)
    email = EmailField(unique=True)
    password = StringField(required=True)
    papers = ListField(ReferenceField(Paper))
    paper_count = IntField(default=1)

    meta = {"indexes": ["email"]}

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.email

    def json(self):
        user = {
            "name": self.username,
            "email": self.email,
            "papers": [paper.getObject() for paper in self.papers],
        }
        return user

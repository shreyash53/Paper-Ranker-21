from mongoengine.document import Document
from mongoengine.fields import (EmailField, ListField, ReferenceField,
                                StringField)
from search.models import Paper


class User(Document):
    username = StringField(required=True)
    email = EmailField(unique=True)
    password = StringField(required=True)
    papers = ListField(ReferenceField(Paper))

    meta = {"indexes": ["email"]}

    def json(self):
        user = {
            "name": self.username,
            "email": self.email,
            "papers": [paper.getObject() for paper in self.papers],
        }
        return user

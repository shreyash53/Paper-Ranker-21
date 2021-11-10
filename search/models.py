
from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField

class Conference(Document):
    name = StringField(required=True)
    abbr = StringField()
    rank = StringField(required=True)

    meta = {
        "indexes": ["name", "abbr"],
    }

    def getObject(self):
        obj = {
            "name": self.name,
            "abbr": self.abbr,
            "rank": self.rank,
        }
        return obj


class Paper(Document):
    title = StringField(required=True)
    author = StringField()
    description = StringField()
    year = IntField()
    conference = ReferenceField(Conference)
    rank = IntField()

    meta = {"indexes": ["title"], "ordering": ["rank"]}

    def getObject(self):
        obj = {
            # "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "conference": self.conference,
            "year": self.year,
        }
        return obj

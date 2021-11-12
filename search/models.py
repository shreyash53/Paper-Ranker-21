from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField, URLField

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
    url = URLField()

    meta = {"indexes": ["title"], "ordering": ["rank"]}

    def getObject(self):
        obj = {
            # "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "conference": self.conference,
            "year": self.year,
            "url": self.url,
        }
        return obj


class RankMeta(Document):
    conference_rank = StringField(required=True, unique=True)
    rank_value = IntField(required=True)

    meta = {"indexes": ["conference_rank"]}

    def get_rank_value(self):
        return self.rank_value

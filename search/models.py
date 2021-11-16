from mongoengine.document import Document
from mongoengine.fields import IntField, ReferenceField, StringField, URLField, ListField, DictField


class Conference(Document):
    name = StringField(required=True)
    abbr = StringField()
    rank = StringField(required=True)

    meta = {
        "indexes": ["abbr"],
    }

    def getObject(self):
        obj = {
            "name": self.name,
            "abbr": self.abbr,
            "rank": self.rank,
        }
        return obj


class Paper(Document):
    paper_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    author = ListField(DictField())
    year = IntField()
    conference = ReferenceField(Conference)
    rank = IntField()
    url = URLField()

    meta = {"indexes": ["paper_id"], "ordering": ["rank"]}

    def getObject(self):
        obj = {
            "title": self.title,
            "author": self.author,
            "conference": self.conference.getObject(),
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

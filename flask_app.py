from flask import Flask, render_template
from search.models import RankMeta
from user.routes import blueprint as user_blueprint
from search.routes import blueprint as search_blueprint
from constants import DB_NAME
from mongoengine.connection import connect
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(search_blueprint)
app.register_blueprint(user_blueprint)


connect(db=DB_NAME)

RankMeta.objects.all().delete()

RankMeta.objects.insert(RankMeta(conference_rank="A+", rank_value = 1))
RankMeta.objects.insert(RankMeta(conference_rank="A", rank_value = 2))
RankMeta.objects.insert(RankMeta(conference_rank="B", rank_value = 3))
RankMeta.objects.insert(RankMeta(conference_rank="C", rank_value = 4))
# RankMeta.objects.insert()
from flask import Flask, render_template
from search.models import RankMeta
from user.routes import blueprint as user_blueprint
from search.routes import blueprint as search_blueprint
from constants import DB_NAME
from mongoengine.connection import connect
from flask_cors import CORS
from flask_login import LoginManager, login_manager
from user.models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
login_manager = LoginManager()
login_manager.init_app(app)

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

@login_manager.user_loader
def load_user(user_email):
    return User.objects(email=user_email).get()
# RankMeta.objects.insert()
from flask import Flask, render_template
from user.routes import blueprint as user_blueprint
from search.routes import blueprint as search_blueprint

app = Flask(__name__)

app.register_blueprint(search_blueprint)
app.register_blueprint(user_blueprint)

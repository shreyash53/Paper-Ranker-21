from flask import Flask, render_template, request
from flask import Blueprint
from user.controller import add_user_paper, login_user
from user.models import User

blueprint = Blueprint("User", __name__, url_prefix="/user")


@blueprint.route("/signup")
def signup():
    return render_template("signup_form.html")


@blueprint.route("/login", methods=["POST"])
def login():
    return login_user(request.json)


@blueprint.route("/add_paper", methods=["POST"])
def add_paper():
    return add_user_paper(request.json)


@blueprint.route("/create_user", methods=["POST"])
def create_user():
    user = User(
        username=request.json.get("name"),
        email=request.json.get("email"),
        password=request.json.get("password"),
    ).save()
    return user.json()

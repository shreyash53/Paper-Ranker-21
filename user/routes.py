from flask import Flask, render_template
from flask import Blueprint
from user.models import User

blueprint = Blueprint('User', __name__)

@blueprint.route("/signup")
def signup():
	return render_template("signup_form.html")

@blueprint.route("/create_user", methods=['POST'])
def create_user():
	return User().signup()

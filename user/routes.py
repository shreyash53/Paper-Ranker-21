from flask import Blueprint, Flask, render_template, request, redirect
from user.controller import add_user_paper, login_user, get_user
from user.models import User
from search.models import Paper
from flask_login import UserMixin, LoginManager, login_manager, login_user, login_required, logout_user, current_user

blueprint = Blueprint("User", __name__, url_prefix="/user")

@blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if current_user is not None and current_user.is_authenticated:
            return redirect("/user/home")
        return render_template("signup/signup.html", data={"error": ""})
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password=request.form.get("password")
        check_user = get_user(email)
        if check_user is not None:
            return render_template("signup/signup.html", data={"error": "User with this email already exists!"})
        user = User(
            username=request.form.get("name"),
            email=request.form.get("email"),
            password=request.form.get("password"),
        ).save()
        login_user(user)
        return redirect("/user/home")

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user is not None and current_user.is_authenticated:
            return redirect("/user/home")
        return render_template("login/login.html", data={"error":None})
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")
        user = get_user(email)
        if user is None:
            return render_template("login/login.html", data={"error":"User not found!"})
        if user.password != password:
            return render_template("login/login.html", data={"error":"Incorrect password!"})
        login_user(user)
        return redirect("/user/home")

@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/user/login")

@blueprint.route("/home", methods=["GET"])
def home():
    if current_user is None or not current_user.is_authenticated:
        return redirect("/user/login")
    return render_template("user/admin.html", data=current_user.json())

@blueprint.route("/add_paper", methods=["POST", "GET"])
@login_required
def add_paper():
    if request.method == "GET":
        return render_template("user/publisher.html", error=None)
    else:
        response = add_user_paper(request.form.to_dict(), current_user)
        if response[1] == 200:
            return redirect("/user/home")
        else:
             return render_template("user/publisher.html", error=response[0])


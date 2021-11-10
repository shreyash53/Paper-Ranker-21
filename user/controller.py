from flask.json import jsonify
from constants import (
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_INTERNAL_SERVER_ERROR,
    HTTP_STATUS_OK,
)
from search.controller import paper_add_helper
from user.models import User
from mongoengine import DoesNotExist


def get_user(user_email):
    try:
        return User.objects(email=user_email).get()
    except DoesNotExist:
        return None


def add_user_paper(request_data):
    user_email = request_data["user_email"]
    user = get_user(user_email)

    if not user:
        return "user_email not found", HTTP_STATUS_BAD_REQUEST

    print(user.json())
    request_data["author"] = user.username
    paper = paper_add_helper(request_data)
    if not paper:
        return "couldn't add paper", HTTP_STATUS_BAD_REQUEST

    try:
        user.papers.append(paper)
        user.save()
    except Exception as e:
        print(e)
        return "Error occured", HTTP_STATUS_INTERNAL_SERVER_ERROR
    return "Operation Successful", HTTP_STATUS_OK


def login_user(request_data):
    email = request_data["email"]
    password = request_data["password"]
    try:
        user = User.objects(email=email, password=password).get()
        return jsonify(user.json()), HTTP_STATUS_OK
    except DoesNotExist:
        return "Incorrect login credentials", HTTP_STATUS_BAD_REQUEST

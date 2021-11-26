from constants import (HTTP_STATUS_BAD_REQUEST,
                       HTTP_STATUS_INTERNAL_SERVER_ERROR, HTTP_STATUS_OK)
from flask.json import jsonify
from mongoengine import DoesNotExist
from search.controller import paper_add_helper, rank_dict
from user.models import User
from search.controller import delete_paper_helper

def get_user(user_email):
    try:
        return User.objects(email=user_email).get()
    except DoesNotExist:
        return None

def add_user_paper(request_data, user):
    conference = request_data["conference"]
    if conference not in rank_dict.keys():
        return (
            "Invalid conference!",
            HTTP_STATUS_BAD_REQUEST,
        )
    request_data["paper_id"] = str(user.id)+str(user.paper_count)
    user.update(set__paper_count= user.paper_count+1)
    paper = paper_add_helper(request_data)
    if paper == False:
        return (
            "Couldn't add paper. another paper with similar title exists",
            HTTP_STATUS_BAD_REQUEST,
        )
    elif not paper:
        return "Error occured", HTTP_STATUS_INTERNAL_SERVER_ERROR
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

def deletePaper(paper_title, user):
    paper = delete_paper_helper(paper_title)
    if paper is None:
        return "Failure to delete", HTTP_STATUS_INTERNAL_SERVER_ERROR
    try:
        user.update(pull__papers=paper)
        print(paper)
        paper.delete()
    except Exception as e:
        print(e)
        return "error", HTTP_STATUS_INTERNAL_SERVER_ERROR
    
    return "Successfully deleted", HTTP_STATUS_OK

def getPapers(user):
    try:
        return jsonify(user.json()['papers']), HTTP_STATUS_OK
    except Exception as e:
        print(e)
        return None, HTTP_STATUS_INTERNAL_SERVER_ERROR
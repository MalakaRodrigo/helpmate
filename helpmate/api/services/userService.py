from flask import jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta
from helpmate.api.utils.userUtils import serialize_document
from helpmate.db import (
    get_users,
    get_user,
    get_user_by_email,
    save_user,
    get_user_session,
    update_user_session,
    save_user_session,
)
import configparser

config = configparser.ConfigParser()


def get_all_users():
    USERS_PER_PAGE = 20
    try:
        (users, total_num_entries) = get_users(
            None, page=0, users_per_page=USERS_PER_PAGE
        )

        user_data = []
        for user in users:
            user_data.append(serialize_document({'email': user['email']}))

        return jsonify(user_data), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


def get_user(user_id):
    try:
        user = get_user(user_id)

        if user is None:
            return (
                jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {"error": "User does not exist"},
                    }
                ),
                400,
            )
        elif user == {}:
            return (
                jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {"error": "Something went wrong"},
                    }
                ),
                500,
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "data": serialize_document(user),
                        "message": {"error": error_message},
                    }
                ),
                200,
            )
    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {"success": False, "data": {}, "message": {"error": error_message}}
            ),
            500,
        )  # Return a JSON error response with a 500 status code for unexpected exceptions


def get_user_by_email_address(email):
    return get_user_by_email(email)


def authenticate_user(post_data):
    try:
        user = serialize_document(get_user_by_email_address(post_data["email"]))
        if user is None:
            return (jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": "Email Address not found"},
                }
            ), 400)
                
        if bcrypt.checkpw(
            post_data["password"].encode("utf-8"), user["password"]
        ):
            prev_session = get_user_session(user["_id"])
            if prev_session:
                # Generate a JWT token with a 1-year expiration time
                expiration_time = datetime.utcnow() + timedelta(seconds=31556926)

                encoded_jwt = jwt.encode(
                    {"id": str(user["_id"]), "exp": expiration_time},
                    "secret4Root",
                    algorithm="HS256",
                )
                payload = {
                    "token": encoded_jwt,
                    "duration": 31556926,
                    "date": datetime.utcnow(),
                }
                update_user_session(prev_session["_id"], payload)
                auth_response = {
                    'userId': user['_id'],
                    'email': user['email'],
                    'name': user['name'],
                    'userRole': user['userRole'],
                }
                return (jsonify(
                    {
                        "success": True,
                        "data": auth_response,
                        "message": {"verity": "Login successful"},
                    }
                ), 200)
            else:
                return (jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {
                            "error": "Session cannot be initilaized, Please contact support."
                        },
                    }
                ), 400)
        else:
            return (jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": "Password is incorrect"},
                }
            ), 400)

    except Exception as e:
        print(e)
        error_message = str(e)
        return (
            jsonify(
                {"success": False, "data": {}, "message": {"error": error_message}}
            ),
            500,
        )

def create_user(post_data):
    try:
        user = get_user_by_email_address(post_data["email"])
        if user is None:
            salt = bcrypt.gensalt(10)  # Generate a salt with a cost factor of 10
            hashed_password = bcrypt.hashpw(post_data["password"].encode("utf-8"), salt)
            payload = {
                "name": post_data["name"],
                "archived" : 0,
                "email": post_data["email"],
                "password": hashed_password,
                "userRole": 2,
                "date": datetime.now(),
            }
            user = save_user(payload)
            if user.acknowledged:
                expiration_time = datetime.utcnow() + timedelta(seconds=31556926)
                encoded_jwt = jwt.encode(
                    {"id": str(user.inserted_id), "exp": expiration_time},
                    "secret4Root",
                    algorithm="HS256",
                )
                session = {
                    "userId": str(user.inserted_id),
                    "archived" : 0,
                    "token": encoded_jwt,
                    "duration": 31556926,
                    "date": datetime.utcnow(),
                }
                save_user_session(session)
                return (jsonify(
                    {
                        "success": True,
                        "data": {
                            "name": post_data["name"],
                            "id": str(user.inserted_id),
                        },
                        "message": {"verify": "User created successfully"},
                    }
                ), 200)
        else:
            return jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": "User already exist"},
                }
            )
    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {"success": False, "data": {}, "message": {"error": error_message}}
            ),
            500,
        )

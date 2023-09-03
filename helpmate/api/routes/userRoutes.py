from flask import Blueprint, request, jsonify
from helpmate.db import get_users, get_user, get_user_by_email, save_user
from bson import ObjectId
from flask_cors import CORS
from helpmate.api.utils.userUtils import validate_login_input, validate_register_input
from datetime import datetime
import bcrypt

users_api_v1 = Blueprint("user_api_v1", "user_api_v1", url_prefix="/api/v1/users")

CORS(users_api_v1)


def serialize_document(doc):
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


@users_api_v1.route("/", methods=["GET"])
def api_get_users():
    USERS_PER_PAGE = 20
    try:
        (users, total_num_entries) = get_users(
            None, page=0, users_per_page=USERS_PER_PAGE
        )

        user_data = []
        for user in users:
            user_data.append(serialize_document(user))

        return jsonify(user_data), 200
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


@users_api_v1.route("/<user_id>", methods=["GET"])
def api_get_user(user_id):
    try:
        user = get_user(user_id)

        if user is None:
            return jsonify({"error": "Not found"}), 400
        elif user == {}:
            return jsonify({"error": "uncaught general exception"}), 400
        else:
            return jsonify(serialize_document(user)), 200
    except Exception as e:
        error_message = str(e)
        return (
            jsonify({"error": error_message}),
            500,
        )  # Return a JSON error response with a 500 status code for unexpected exceptions


@users_api_v1.route("/", methods=["POST"])
def api_authenticate_user():
    try:
        post_data = request.get_json()
        validation_result = validate_login_input(post_data)
        errors = validation_result["errors"]
        is_valid = validation_result["is_valid"]
        if is_valid:
            user = get_user_by_email(post_data["email"])
            if user is None:
                return jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {"error": "Email Address not found"},
                    }
                )
            if bcrypt.checkpw(
                post_data["password"].encode("utf-8"), user["password"].encode("utf-8")
            ):
                return jsonify(
                    {
                        "success": True,
                        "data": serialize_document(user),
                        "message": {"verity": "Login successful"},
                    }
                )
            else:
                return jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {"error": "Password is incorrect"},
                    }
                )

        else:
            # Loop through and print validation error messages
            for field, message in errors.items():
                print(f"Validation Error in field '{field}': {message}")
        return jsonify(
            {
                "success": False,
                "data": errors,
                "message": {"error": "Invalid credentials"},
            }
        )

    except Exception as e:
        error_message = str(e)
        return (
            jsonify({"success": False, "data": {}, "error": error_message}),
            500,
        )


@users_api_v1.route("/create", methods=["POST"])
def api_create_user():
    try:
        post_data = request.get_json()
        validation_result = validate_register_input(post_data)
        errors = validation_result["errors"]
        is_valid = validation_result["is_valid"]
        if is_valid:
            user = get_user_by_email(post_data["email"])
            if user is None:
                salt = bcrypt.gensalt(10)  # Generate a salt with a cost factor of 10
                hashed_password = bcrypt.hashpw(
                    post_data["password"].encode("utf-8"), salt
                )
                payload = {
                    "name": post_data["name"],
                    "email": post_data["email"],
                    "password": hashed_password,
                    "userRole": 2,
                    "date": datetime.now(),
                }
                user = save_user(payload)
                if user.acknowledged:
                    print(user.inserted_id)
                    return jsonify(
                        {
                            "success": True,
                            "data": {
                                "name": post_data["name"],
                                "id": str(user.inserted_id)
                            },
                            "message": {"verify": "User created successfully"},
                        }
                    )
            else:
                return jsonify(
                    {
                        "success": False,
                        "data": {},
                        "message": {"error": "User already exists"},
                    }
                )

        else:
            # Loop through and print validation error messages
            for field, message in errors.items():
                print(f"Validation Error in field '{field}': {message}")

    except Exception as e:
        error_message = str(e)
        return (
            jsonify({"success": False, "data": {}, "error": error_message}),
            500,
        )  # Return a JSON error response with a 500 status code for unexpected exceptions

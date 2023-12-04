from flask import Blueprint, request, jsonify
from helpmate.api.validators.userValidators import validate_login_input, validate_register_input
from helpmate.api.services.userService import (
    get_all_users,
    get_user,
    authenticate_user,
    create_user,
)

users_api_v1 = Blueprint("user_api_v1", "user_api_v1", url_prefix="/api/v1/users")

@users_api_v1.route("/", methods=["GET"])
def api_get_users():
    return get_all_users()


@users_api_v1.route("/<user_id>", methods=["GET"])
def api_get_user(user_id):
    try:
        return get_user(user_id)
    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": error_message},
                }
            ),
            500,
        )


@users_api_v1.route("/", methods=["POST"])
def api_authenticate_user():
    try:
        post_data = request.get_json()
        validation_result = validate_login_input(post_data)
        errors = validation_result["errors"]
        is_valid = validation_result["is_valid"]
        if is_valid:
            return authenticate_user(post_data)
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
            jsonify(
                {
                    "success": False,
                    "data": {},
                    "message": {"error": error_message},
                }
            ),
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
            return create_user(post_data)
        else:
            # Loop through and print validation error messages
            for field, message in errors.items():
                print(f"Validation Error in field '{field}': {message}")
            return jsonify(
                {
                    "success": False,
                    "data": errors,
                    "error": errors[0],
                    "message": {"error": "Invalid credentials"},
                }
            )
    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {
                    "success": False,
                    "data": {},
                    "error": error_message,
                    "message": "Something went wrong",
                }
            ),
            500,
        )  # Return a JSON error response with a 500 status code for unexpected exceptions

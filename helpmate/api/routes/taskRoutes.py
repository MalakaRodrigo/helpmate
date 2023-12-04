from flask import Blueprint, request, jsonify
from helpmate.api.services.taskService import save_new_task, get_tasks


tasks_api_v1 = Blueprint("task_api_v1", "task_api_v1", url_prefix="/api/v1/tasks")


@tasks_api_v1.route("/create", methods=["POST"])
def api_save_task():
    try:
        post_data = request.get_json()
        task = save_new_task(post_data)
        return (
            jsonify(
                {
                    "success": True,
                    "data": task,
                    "message": {},
                }
            ),
            200,
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


@tasks_api_v1.route("/", methods=["POST"])
def api_get_tasks():
    try:
        post_data = request.get_json()
        print(post_data["taskIds"])
        tasks = get_tasks({"task_ids" : post_data["taskIds"]})
        return (
            jsonify(
                {
                    "success": True,
                    "data": {"tasks": tasks},
                    "message": {},
                }
            ),
            200,
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

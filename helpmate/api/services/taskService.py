from flask import jsonify
from helpmate.api.utils.userUtils import serialize_document
from helpmate.db import save_task, get_all_tasks, get_tasks_by_ids
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import configparser

config = configparser.ConfigParser()


def get_tasks(task_ids):
    try:
        task_ids = task_ids.get("task_ids", [])  # Get the task_ids array from payload

        if len(task_ids) == 0:
            # If task_ids array is empty, return all tasks
            return get_all_tasks()
        else:
            # Convert string IDs to ObjectId if needed
            object_ids = [ObjectId(task_id) for task_id in task_ids]
            return get_tasks_by_ids(object_ids)
    except Exception as e:
        print(e)
        error_message = str(e)
        return (
            jsonify(
                {"success": False, "data": {}, "message": {"error": error_message}}
            ),
            500,
        )


def save_new_task(post_data):
    try:
        payload = post_data
        payload["created"] = datetime.utcnow()
        payload["percentage"] = 0
        payload["quality"] = 0
        payload["archived"] = 0
        inserted_task = save_task(payload)
        if inserted_task.acknowledged:
            tasks = get_tasks({"task_ids": [str(inserted_task.inserted_id)]})
            return {
                "success": True,
                "data": tasks,
                "message": {"verify": "Task created successfully"},
            }

        else:
            {
                "success": False,
                "data": {},
                "message": {"error": "Task Creation Failed"},
            }

    except Exception as e:
        error_message = str(e)
        return (
            jsonify(
                {"success": False, "data": {}, "message": {"error": error_message}}
            ),
            500,
        )

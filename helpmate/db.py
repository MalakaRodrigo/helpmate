from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def build_query_sort_project(filters):
    query = {}
    sort = [("tomatoes.viewer.numReviews", -1)]
    project = None
    if filters:
        if "text" in filters:
            query = {"$text": {"$search": filters["text"]}}
            meta_score = {"$meta": "textScore"}
            sort = [("score", meta_score)]
            project = {"score": meta_score}
        elif "cast" in filters:
            query = {"cast": {"$in": filters["cast"]}}
        elif "genres" in filters:
            query = {}

    return query, sort, project


## User routes
def get_users(filters, page, users_per_page):
    query, sort, project = build_query_sort_project(filters)
    if project:
        cursor = db.users.find(query, project).sort(sort)
    else:
        cursor = db.users.find(query).sort(sort)

    total_num_users = 0
    if page == 0:
        total_num_users = db.users.count_documents(query)

    users = cursor.limit(users_per_page)

    return (list(users), total_num_users)


def get_user(id):
    try:
        pipeline = [{"$match": {"_id": ObjectId(id), "archived" :0}}]

        user = db.users.aggregate(pipeline).next()
        return user

    except StopIteration as _:
        return None

    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}


def get_user_by_email(email):
    try:
        user = db.users.find_one({"email": email, "archived" :0})
        return user
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}


def save_user(payload):
    try:
        return db.users.insert_one(payload)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}

def delete_user(user_id):
    try:
        return db.users.update_one( {"_id": user_id},
            {
                "$set": {
                    "archived": 1,
                }
            },)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}


# session routes
def get_user_session(user_id):
    try:
        session = db.sessions.find_one({"userId": str(user_id), "archived" :0})
        return session
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}


def save_user_session(payload):
    try:
        session = db.sessions.insert_one(payload)
        return session
    except Exception as e:
        error_message = str(e)
        print(error_message)


def update_user_session(session_id, payload):
    try:
        session = db.sessions.update_one(
            {"_id": session_id},
            {
                "$set": {
                    "token": payload["token"],
                    "duration": payload["duration"],
                    "date": payload["date"],
                }
            },
        )
        return session
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}


def save_task(payload):
    try:
        return db.tasks.insert_one(payload)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}

def get_all_tasks():
    try:
        tasks = db.tasks.find({"archived": 0})
        return list(tasks)  # Convert Cursor to a list of tasks
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}

def get_tasks_by_ids(object_ids):
    try:
        tasks = db.tasks.find({"_id": {"$in": object_ids}, "archived": 0})
        return list(tasks)  # Convert Cursor to a list of tasks
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return {}
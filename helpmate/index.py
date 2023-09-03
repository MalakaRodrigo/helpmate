import os
from flask import Flask, render_template
from json import JSONEncoder
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from bson import json_util, ObjectId
from datetime import datetime
from helpmate.api.routes.userRoutes import users_api_v1

# Custom JSON Encoder to handle special types (datetime, ObjectId)
class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


# Function to create and configure the Flask app
def create_app():
    # Define directory paths
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build')

    # Create the Flask app
    app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app)

    # Configure JWT (JSON Web Tokens) for authentication
    JWTManager(app)

    # Set the JSON encoder to the custom MongoJsonEncoder
    app.json_encoder = MongoJsonEncoder

    # Register API routes
    app.register_blueprint(users_api_v1)

    # Uncomment the following lines if you want to serve a single-page app (React, Angular, etc.)
    # This will serve the 'index.html' file for all routes, enabling client-side routing
    # Note: This is useful for single-page applications where routing is handled on the client-side.
    # @app.route('/', defaults={'path': ''})
    # @app.route('/<path:path>')
    # def serve(path):
    #     return render_template('index.html')

    return app
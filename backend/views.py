import os
from flask import request, Blueprint, send_from_directory, render_template, request, jsonify
import os
from flask_login import login_required, current_user
from bson import ObjectId 
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def serve_react(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    react_build_dir = os.path.join(base_dir, "../frontend/build")
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")
    

@views.route('/save_search', methods=['POST'])
@login_required
def save_search():
    """
    Save the search terms the user inputs into the database.
    """
    data = request.get_json()
    if not data or 'departure' not in data or 'arrival' not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_search = {
        # "user_id": ObjectId(current_user.id),
        "departure_dest": data['departure'],
        "arrival_dest": data['arrival'],
        "search_datetime": datetime.now(),
    }
    views.saved_search_collection.insert_one(new_search)
    return jsonify({"message": "Search saved successfully"}), 201


@views.route('/get_routes', methods=['GET'])
@login_required
def get_routes():
    """
    Retrieve all JSON values saved for the current user.
    """
    # user_id = ObjectId(current_user.id)
    saved_searches = list(views.generated_search_collection.find())

    return jsonify(saved_searches), 200
    
import os
from flask import request, Blueprint, send_from_directory
import os

routes = Blueprint('views', __name__)

@routes.route("/", defaults={"path": ""})
@routes.route("/<path:path>")
def serve_react(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    react_build_dir = os.path.join(base_dir, "../frontend/build")
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")
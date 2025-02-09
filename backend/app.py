from flask import Flask, send_from_directory
from .database import db
import os

from flask import Flask, request, jsonify
# from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "summaries.db")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/your_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #set up routes
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
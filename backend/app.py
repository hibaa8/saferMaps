from flask import Flask
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
from flask import current_app, g
from pymongo import MongoClient
from flask_cors import CORS

mongo = PyMongo()
load_dotenv()

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
    app.config['MONGO_URI'] = os.getenv('MONGO_URI') 
    app.config['DEBUG'] = True

    client = MongoClient(os.getenv('MONGO_URI'))
    print(client)
    db = client['map_routes']
    users_collection = db['User']
    print(users_collection)
    generated_search_collection = db['GeneratedSearch']
    saved_search_collection = db['SavedSearch']

    from views import views
    # from auth import auth
    # auth.users_collection = users_collection
    views.generated_search_collection = generated_search_collection
    views.saved_search_collection = saved_search_collection

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')
    
    return app

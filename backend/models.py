from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class SearchHistory(db.Model):
    __tablename__ = 'SearchHistory'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    departure_dest = db.Column(db.String(50), unique=True, nullable=False)
    arrival_dest = db.Column(db.String(50), unique=True, nullable=False)
    search_datetime = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class GeneratedSearch(db.Model):
    __tablename__ = 'GeneratedSearch'
    id = db.Column(db.Integer, primary_key=True)
    route_json = db.Column(db.JSON, nullable=False)

class SavedSearch(db.Model):
    __tablename__ = 'SavedSearch'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    search_data = db.Column(db.JSON, nullable=False)
    screenshot = db.Column(db.String(255))  
    user = db.relationship('User', backref='saved_searches')



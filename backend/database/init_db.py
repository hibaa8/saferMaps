from backend.app import create_app
from database import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized successfully.")
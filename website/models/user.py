from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime
from flask_login import UserMixin
from enum import unique

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    notes = db.relationship("Note")
    todos = db.relationship("ToDo")
    reminders = db.relationship("Reminder")
    videos = db.relationship("Video")

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}"
        # return '<User %r>' % self.id

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def format_user(user):
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "first_name": user.first_name,
            "last_name": user.last_name
        }

    # def is_authenticated(self):
    #     return True

    # def is_active(self):
    #     return True

    # def is_anonymous(self):
    #     return False
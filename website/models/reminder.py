from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime
from enum import unique

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User", back_populates="reminder")

    def __repr__(self):
        return '<Reminder %r>' % self.id

    def __init__(self, description, user_id):
        self.description = description
        self.user_id = user_id

    def format_reminder(reminder):
        return {
            "id": reminder.id,
            "description": reminder.description,
            "date_created": reminder.date_created,
            "user_id": reminder.user_id
        }
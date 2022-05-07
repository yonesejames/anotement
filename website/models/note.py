from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime
from enum import unique
from flask_login import UserMixin

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User", back_populates="note")

    def __repr__(self):
        return '<Note %r>' % self.id

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id

    def format_note(note):
        return {
            "id": note.id,
            "text": note.text,
            "date_created": note.date_created,
            "user_id": note.user_id
        }
from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime
from enum import unique

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User", back_populates="todo")

    def __repr__(self):
        return '<Task %r>' % self.id

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def format_todo(todo):
        return {
            "id": todo.id,
            "content": todo.content,
            "completed": todo.completed,
            "date_created": todo.date_created,
            "user_id": todo.user_id
        }
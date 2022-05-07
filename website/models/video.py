from website.extensions import db
from sqlalchemy.sql import func
from datetime import datetime
from enum import unique

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship("User", back_populates="videos")

    def __repr__(self):
        return '<Video %r>' % self.id

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id

    def format_video(video):
        return {
            "id": video.id,
            "url": video.url,
            "date_created": video.date_created,
            "user_id": video.user_id,
        }
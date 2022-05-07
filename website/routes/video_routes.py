from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from website.extensions import db
from website.models.video import Video
import json

video = Blueprint("video", __name__, url_prefix="/videos")

#view all videos
@video.route("/", methods=["GET"])
@login_required
def view_videos():
    video = Video.query.order_by(Video.id.asc()).all()
    return render_template("video.html", video=video, user=current_user)


#view a video
@video.route("/<int:id>", methods=["GET"])
@login_required
def view_video(id):
    video = Video.query.filter_by(id=id).one()
    return render_template("video.html", video=video, user=current_user)


#create a video
@video.route("/", methods=["POST"])
@login_required
def create_video():
    video = request.form.get("video")
    new_video = Video(url=video, user_id=current_user.id)

    if len(video) < 1:
        flash("Note is too short!", category="error")
    else:
        try:
            db.session.add(new_video)
            db.session.commit()
            flash("Video added!", category="success")
            return redirect(url_for("video.view_videos"))
        except:
            return "There was an issue creating your video. Please try again."

    return render_template("video.html", video=video, user=current_user)


#delete a video
@video.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_video(id):
    video_to_delete = video.query.filter_by(id=id).one()
    try:
        db.session.delete(video_to_delete)
        db.session.commit()
        flash("video deleted!", category="success")
        return redirect(url_for("video.view_videos"))        
    except:
        return "There was an issue deleting your video. Please try again."

    return render_template("video.html", video=video, user=current_user)



#update a video
@video.route("/update-videos/<int:id>", methods=["PUT"])
@login_required
def update_videos(id):
    videos = Video.query.filter_by(id=id)
    url = request.json["url"]
    try:
        videos.update(dict(url=url, date_created=datetime.utcnow()))
        flash("video updated!", category="success")
        return redirect(url_for("video.view_videos"))
    except:
        return "There was an issue updating your video. Please try again."

    return render_template("video.html", video=video, user=current_user)

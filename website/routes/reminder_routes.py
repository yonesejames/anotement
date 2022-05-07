from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from website.extensions import db
from website.models.reminder import Reminder
import json

reminder = Blueprint("reminder", __name__, url_prefix="/reminders")

#view all reminders
@reminder.route("/", methods=["GET"])
@login_required
def view_reminders():
    reminder = Reminder.query.order_by(Reminder.id.asc()).all()
    return render_template("reminder.html", reminder=reminder, user=current_user)


#view a reminder
@reminder.route("/<int:id>", methods=["GET"])
@login_required
def view_reminder(id):
    reminder = Reminder.query.filter_by(id=id).one()
    return render_template("reminder.html", reminder=reminder, user=current_user)


#create a reminder
@reminder.route("/", methods=["POST"])
@login_required
def create_reminder():
    reminder = request.form.get("reminder")

    if len(reminder) < 1:
        flash("reminder is too short!", category="error")
    else:
        try:
            new_reminder = Reminder(description=reminder, user_id=current_user.id)
            db.session.add(new_reminder)
            db.session.commit()
            flash("reminder added!", category="success")
            return redirect(url_for("reminder.view_reminders"))
        except:
            return "There was an issue creating your reminder. Please try again."
    return render_template("reminder.html", reminder=reminder, user=current_user)


#delete a reminder
@reminder.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_reminder(id):
    reminder_to_delete = Reminder.query.filter_by(id=id).one()
    try:
        db.session.delete(reminder_to_delete)
        db.session.commit()
        flash("reminder deleted!", category="success")
        return redirect(url_for("reminder.view_reminders"))        
    except:
        return "There was an issue deleting your reminder. Please try again"

    return render_template("reminder.html", reminder=reminder, user=current_user)


#update a reminder
@reminder.route("/update/<int:id>", methods=["PUT"])
@login_required
def update_reminder(id):
    reminder = Reminder.query.filter_by(id=id)
    description = request.json["description"]
    try:
        reminder.update(dict(description=description, date_created=datetime.utcnow()))
        flash("reminder updated!", category="success")
        return redirect(url_for("reminder.view_reminders")) 
    except:
        return "There was an issue updating your reminder. Please try again."
    
    return render_template("reminder.html", reminder=reminder, user=current_user)

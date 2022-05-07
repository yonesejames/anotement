from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime
from website.extensions import db
from website.models.note import Note
from flask_login import login_required, current_user
import json

note = Blueprint("note", __name__, url_prefix="/notes")


#view all notes
@note.route("/", methods=["GET"])
@login_required
def view_notes():
    return render_template("note.html", user=current_user)


#view a note
@note.route("/<int:id>", methods=["GET"])
@login_required
def view_note(id):
    note = Note.query.filter_by(id=id).one()
    return render_template("note.html", note=note)


#create a note
@note.route("/", methods=["POST"])
@login_required
def create_note():
    note = request.form.get("note")

    if len(note) < 1:
        flash("Note is too short!", category="error")
    else:
        try:
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
        except:
            return "There was an issue creating your note. Please try again."

    note = Note.query.order_by(Note.id.asc()).all()       
    return render_template("note.html", note=note, user=current_user)


@note.route("/delete/<int:id>")
def delete(id):
    note_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect("/notes")
    except:
        return "There was an issue deleting your task. Please try again."


@note.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        note.text = request.form["text"]
        try:
            db.session.commit()
            return redirect("/notes")
        except:
            return "There was an issue updating your note. Please try again."
    else:
        return render_template("note_update.html", note=note, user=current_user)



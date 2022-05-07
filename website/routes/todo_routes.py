from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from website.extensions import db
from website.models.todo import ToDo
import json

todo = Blueprint("todo", __name__, url_prefix="/to-do")

# #view all tasks
# @todo.route("/", methods=["GET"])
# @login_required
# def view_tasks():
#     return render_template("todo.html", user=current_user)


#view a task
@todo.route("/<int:id>", methods=["GET"])
@login_required
def view_task(id):
    task = ToDo.query.filter_by(id=id).one()
    return render_template("todo.html", task=task, user=current_user)


#view all tasks and create a task
@todo.route("/", methods=["POST", "GET"])
@login_required
def create_task():
    if request.method == "POST":
        task_content = request.form["content"]

        if len(task_content) < 1:
            flash("Task is too short!", category="error")
        else:
            try:
                new_task = ToDo(content=task_content, user_id=current_user.id)
                db.session.add(new_task)
                db.session.commit()
                flash("Task added!", category="success")
                return redirect("/to-do")
            except:
                return "There was an issue creating your task. Please try again."
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("todo.html", tasks=tasks, user=current_user)


@todo.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/to-do")
    except:
        return "There was an issue deleting your task. Please try again."


@todo.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/to-do/")
        except:
            return "There was an issue updating your task. Please try again."
    else:
        return render_template("todo_update.html", task=task, user=current_user)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.extensions import db
from datetime import datetime
from website.models.user import User
from flask_login import login_required, current_user

user = Blueprint("user", __name__, url_prefix="/user")


#view a user
@user.route("/<int:id>", methods=["GET"])
@login_required
def view_user(id):
    user = User.query.filter_by(id=id).one()
    return render_template("user.html", user=user)
    # formatted_user = User.format_user(user)
    # return formatted_user 

# UNABLE TO DELETE A USER AT THIS TIME:
#delete a user
# @user.route("/delete/<int:id>", methods=["DELETE"])
# @login_required
# def delete_user(id):
#     user_to_delete = User.query.filter_by(id=id).one()
#     try:
#         db.session.delete(user_to_delete)
#         db.session.commit()
#         flash("Account deleted!", category="success")
#         return redirect(url_for("page.view_sign_up"))        
#     except:
#         return "There was an issue deleting your account. Please try again."
    
    # return render_template("user.html", user=user, user=current_user)


# UNABLE TO UPDATE A USER AT THIS TIME:
#update a user
# @user.route("/update/<int:id>", methods=["PUT"])
# @login_required
# def update_user(id):
#     user = User.query.filter_by(id=id)
#     email = request.json["email"]
#     first_name = request.json["first_name"]
#     last_name = request.json["last_name"]
#     try:
#         user.update(dict(email=email, first_name=first_name, last_name=last_name, date_created=datetime.utcnow()))
#         flash("user updated!", category="success")
#         return redirect(url_for("page.view_sign_up")) 
#     except:
#         return "There was an issue updating your account. Please try again."
    
    # return render_template("user.html", user=user, user=current_user)

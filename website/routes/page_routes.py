from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.extensions import db
from website.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from xmlrpc.client import boolean
from flask_login import login_user, login_required, logout_user, current_user

page = Blueprint("page", __name__, url_prefix="/")


@page.route("/", methods=["GET"])
def index():
    return render_template("index.html", user=current_user)


@page.route("/why", methods=["GET"])
def why():
    return render_template("why.html", user=current_user)


@page.route("/product", methods=["GET"])
def product():
    return render_template("product.html", user=current_user)


@page.route("/plans", methods=["GET"])
def plans():
    return render_template("plans.html", user=current_user)


#login page
@page.route("/login", methods=["GET"])
def view_login():
    return render_template("login.html", user=current_user)


@page.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("page.dashboard"))
        else:
            flash("Incorrect password, please try again.", category="error")
    else:
        flash("Email does not exist, please sign up.", category="error")

    return render_template("login.html", user=current_user)


#logout page
@page.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("page.login"))


#signup page
@page.route("/sign-up", methods=["GET"])
def view_sign_up():
    return render_template("sign_up.html", user=current_user)


@page.route("/sign-up", methods=["POST"])
def sign_up():
    email = request.form.get("email")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email already exists.", category="error")
    elif len(email) <= 5:
        flash("Email must be greater than 5 characters.", category="error")
    elif len(first_name) <= 1 or len(last_name) <= 1:
        flash("Name must be greater than 1 character.", category="error")
    elif password1 != password2:
        flash("Passwords do not match.", category="error")
    elif len(password1) <= 5:
        flash("Password must be greater than 5 characters.", category="error")
    else:
        new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method="sha256"))
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)
        flash("Account Created!", category="success")
        return redirect(url_for("page.dashboard"))

    return render_template("sign_up.html", user=current_user)


@page.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

from flask import Blueprint, redirect, render_template, url_for, abort, request
from flask_login import login_required, login_user, logout_user, current_user, login_manager
from marshmallow.exceptions import ValidationError
from main import db, lm
from models.users import User
from schemas.user_schema import users_schema, user_schema, user_update_schema

@lm.user_loader
def load_user(user):
    return User.query.get(user)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/users/login/')

users = Blueprint('users', __name__)

@users.route("/users/", methods=["GET"])
def get_users():
    data = {
        "page_title": "user Index",
        "users": users_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data = data)

@users.route("/users/signup/", methods = ["GET", "POST"])
def sign_up():
    data = {"page_title": "Sign Up"}

    if request.method == "GET":
        return render_template("signup.html", page_data = data)

    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for("users.get_users"))

@users.route("/users/login/", methods = ["GET", "POST"])
def log_in():
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("login.html", page_data = data)

    user = User.query.filter_by(email=request.form["email"]).first()
    if user and user.check_password(password=request.form["password"]):
        login_user(user)
        return redirect(url_for('blogs.get_blogs'))

    abort(401, "Login unsuccessful. Please check the user email and password")

@users.route("/users/account/", methods=["GET", "POST"])
@login_required
def user_detail():
    if request.method == "GET":
        data = {"page_title": "Account Details"}
        return render_template("user_detail.html", page_data = data)

    user = User.query.filter_by(user_id=current_user.user_id)
    updated_fields = user_schema.dump(request.form)
    errors = user_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message=errors)

    user.update(updated_fields)
    db.session.commit()
    return redirect(url_for("users.get_users"))

@users.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("users.log_in"))
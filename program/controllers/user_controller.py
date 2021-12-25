from flask import Blueprint, redirect, render_template, url_for, abort, request, flash
from flask_login import login_required, login_user, logout_user, current_user, login_manager
from marshmallow.exceptions import ValidationError
from main import db, lm
from models.users import User
from schemas.user_schema import users_schema, user_schema, user_update_schema
from forms import LoginForm


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
        "page_title": "User Index",
        "users": users_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data=data)


@users.route("/users/signup/", methods=["GET", "POST"])
def sign_up():
    data = {"page_title": "Sign Up"}

    if request.method == "GET":
        return render_template("signup.html", page_data=data)

    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for("users.get_users"))


@users.route("/users/login/", methods=["GET", "POST"])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('blogs.get_blogs'))
    form = LoginForm()

    data = {
        "page_title": "Log In",
        "form" : form
    }

    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users.log_in'))
        login_user(user, remember=form.remember_me.data)
        #flash(f'Login requested for user {form.username.data}, \
        #remember_me={form.remember_me.data}' )
        return redirect(url_for('blogs.get_blogs'))

    data = {
        "page_title": "Log In",
        "form" : form
    }
    #if request.method == "GET":
    return render_template("login.html", page_data=data)


@users.route("/users/<int:user_id>/", methods=["GET", "POST"])
@login_required
def user_detail(user_id):
    view_user = User.query.get_or_404(user_id)
    if request.method == "GET":
        data = {
            "page_title": f"Hi, { current_user.user_name }",
            "user" : view_user
        }
        return render_template("user_detail.html", page_data=data)

    user = User.query.get_or_404(user_id)
    updated_fields = user_schema.dump(request.form)
    errors = user_update_schema.validate(updated_fields)
    
    if errors:
        raise ValidationError(message=errors)

    user.update(updated_fields)
    db.session.commit()
    return redirect(url_for("users.get_users"))

@users.route("/users/follow/<int:user_id>/", methods=["POST"])
@login_required
def follow(user_id):
    
    target_user = User.query.get_or_404(user_id)
    if target_user is None:
        return redirect(url_for('users.get_users'))
    if not current_user.is_following(target_user):
        current_user.follow(target_user)
        db.session.commit()
        
    return redirect(url_for('users.user_detail', user_id=user_id))

@users.route("/users/unfollow/<int:user_id>/", methods=["POST"])
@login_required
def unfollow(user_id):
    
    target_user = User.query.get_or_404(user_id)
    if target_user is None:
        return redirect(url_for('users.get_users'))
    if current_user.is_following(target_user):
        current_user.unfollow(target_user)
        db.session.commit()
        
    return redirect(url_for('users.user_detail', user_id=user_id))

@users.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("users.log_in"))

@users.route("/users/delete/", methods=["POST"])
@login_required
def delete_user():
    current_id = current_user.user_id
    logout_user()
    user = User.query.get_or_404(current_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("blogs.get_blogs"))

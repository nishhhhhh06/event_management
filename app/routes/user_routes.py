from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from app.extensions import db
from app.forms import UpdateUserForm

user_bp = Blueprint("users", __name__)


@user_bp.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not all([username, email, password, role]):
            flash("All fields are required!", "danger")
            return redirect(url_for("users.create_user"))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists!", "warning")
            return redirect(url_for("users.create_user"))

        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {username} created successfully!", "success")
        return redirect(url_for("users.list_users"))

    return render_template("create_user.html")


@user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user and user.role != "admin":  # Prevent deleting admins
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user {user.username}", "danger")
    return redirect(url_for("users.list_users"))


@user_bp.route("/list_users")
@login_required
def list_users():
    if current_user.role != "admin":
        flash("Access Denied! Only admins can view users.", "danger")
        return redirect(url_for("events.list_events"))

    users = User.query.all()
    return render_template("list_users.html", users=users)


@user_bp.route("/update_user/<int:user_id>", methods=["POST"])
def update_user(user_id):
    user = User.query.get(user_id)
    if user and user.role != "admin":  # Prevent changing admin role
        new_role = request.form.get("role")
        if new_role in ["organizer", "attendee"]:
            user.role = new_role
            db.session.commit()
            flash(f"Updated {user.username} to {new_role.capitalize()}", "success")
    return redirect(url_for("users.list_users"))

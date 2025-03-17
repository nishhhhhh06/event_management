from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from app.models import User
from app.extensions import db, bcrypt
from app.forms import RegisterForm, LoginForm


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("No account found with this email. Please register first.", "danger")
            return redirect(url_for("auth.login"))

        if not user.check_password(form.password.data):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user,  remember=True)
        session.permanent = True
        flash("Login successful!", "success")
        return redirect(url_for("events.list_events"))

    if form.errors:
        if "email" in form.errors:
            flash("Invalid email format. Please enter a valid email address.", "danger")
        if "password" in form.errors:
            flash("Invalid password format. Please check your password.", "danger")

    return render_template("auth.html", form=form, login=True)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "danger")
            return redirect(url_for("auth.register"))

        # Create a new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    if form.errors:
        if "email" in form.errors:
            flash("Invalid email format. Please enter a valid email address.", "danger")
        if "password" in form.errors:
            flash("Password does not meet the requirements.", "danger")
        if "username" in form.errors:
            flash("Invalid username. Please use a valid format.", "danger")

    return render_template("auth.html", form=form, login=False)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

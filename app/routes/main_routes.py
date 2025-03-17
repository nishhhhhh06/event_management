from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.forms import LoginForm, RegisterForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home():
    if current_user.is_authenticated:
        return redirect(url_for("events.list_events"))
    form = LoginForm()
    return render_template("auth.html", form=form, login=True)

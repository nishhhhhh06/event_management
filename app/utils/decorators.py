from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from flask_mail import Message
from app.extensions import mail


def role_required(role):
    # for role-based access control
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = get_jwt_identity().get("role")
            if user_role != role and user_role != "admin":
                return jsonify({"message": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)

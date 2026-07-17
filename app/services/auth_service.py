from app.extensions import db
from app.models.user import User, UserRole
from app.utils.helpers import success_response, error_response
from flask_jwt_extended import create_access_token

VALID_ROLES = {role.value for role in UserRole}


def register_user(fullname, email, password, role):

    # Required fields
    if not all([fullname, email, password, role]):
        return {
            "success": False,
            "message": "All fields are required."
        }

    # Role validation
    if role not in VALID_ROLES:
        return {
            "success": False,
            "message": "Invalid role."
        }

    # Email uniqueness
    if User.query.filter_by(email=email).first():
        return {
            "success": False,
            "message": "Email already exists."
        }

    # Create user
    user = User(
        fullname=fullname,
        email=email,
        role=UserRole(role)
    )

    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {
            "success": False,
            "message": "An error occurred while registering the user."
        }

    return {
        "success": True,
        "message": "Registration successful.",
        "data": user.to_dict()
    }

def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {
            "success": False,
            "message": "Invalid email or password."
        }
    
    login_token = create_access_token(identity=user.id)
    
    return {
        "success": True,
        "message": "Login successful.",
        "data": {**user.to_dict(), "access_token": login_token}
    }

from app.extensions import db
from app.models.user import User, UserRole

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

    db.session.add(user)
    db.session.commit()

    return {
        "success": True,
        "message": "Registration successful.",
        "data": user.to_dict()
    }
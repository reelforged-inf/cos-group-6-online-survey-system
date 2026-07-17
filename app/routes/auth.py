from flask import Blueprint, request
from app.services.auth_service import register_user, login_user
from app.utils.helpers import success_response, error_response

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

@auth_bp.post("/register")
def register():
    data = request.get_json()

    if not data:
        return error_response(
        "Request body must be valid JSON."
    )
    result = register_user(
        fullname=data.get("fullname"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
    )
    if not result["success"]:
        return error_response(result["message"], status_code=400)
    
    return success_response(result["message"], data=result["data"], status_code=201)

@auth_bp.post("/login")
def login():
    data = request.get_json()

    if not data:
        return error_response(
            "Request body must be valid JSON."
        )
    
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response(
            "Email and password are required fields.", status_code=400
        )

    result = login_user(email=email, password=password)
    if not result["success"]:
        return error_response(result["message"], status_code=401)

    return success_response(result["message"], data=result["data"], status_code=200)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    # Implement logout logic 
    return success_response("Logout successful.", status_code=200)
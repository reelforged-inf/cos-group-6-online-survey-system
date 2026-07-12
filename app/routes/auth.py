from flask import Blueprint, request
from app.services.auth_service import register_user
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
    success = register_user(
        fullname=data.get("fullname"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
    )
    if not success["success"]:
        return error_response(success["success"], status_code=400)
    
    return success_response(success["message"], data=success["data"], status_code=201)
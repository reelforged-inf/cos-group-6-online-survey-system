from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "message": "HexaSurvey Backend API is running."
    }), 200
from flask import jsonify


def success_response(message, data=None, status_code=200):
    """
    Standard success response.
    """
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code


def error_response(message, errors=None, status_code=400):
    """
    Standard error response.
    """
    return jsonify({
        "success": False,
        "message": message,
        "errors": errors
    }), status_code
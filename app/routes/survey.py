from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, UserRole
from app.extensions import db
from app.services.survey_service import (create_survey,  get_creator_surveys, get_survey, update_survey, delete_survey, get_shared_survey)
from app.services.response_service import submit_response
from app.services.analytics_service import get_survey_analytics_service
from app.services.email_service import send_survey_invitations
from app.utils.helpers import success_response, error_response


survey_bp = Blueprint(
    "survey",
    __name__,
    url_prefix="/api/surveys"
)


def get_current_creator_id():
    """Return the authenticated creator's ID or deny access."""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user or user.role != UserRole.CREATOR:
        raise PermissionError("Only creators can access this route.")

    return user_id


@survey_bp.route("", methods=["POST"])
@jwt_required()
def create():

    try:
        data = request.get_json()

        creator_id = get_current_creator_id()

        survey = create_survey(
            data=data,
            creator_id=creator_id
        )

        return success_response(
            message="Survey created successfully.",
            data={
                "id": survey.id,
                "share_token": survey.share_token
            },
            status_code=201
        )

    except PermissionError as e:
        return error_response(message=str(e), status_code=403)

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/", methods=["GET"])
@jwt_required()
def get_surveys():

    try:
        creator_id = get_current_creator_id()


        surveys = get_creator_surveys(creator_id)

        return success_response(
            message="Surveys retrieved successfully.",
            data=[
                {
                    "id": survey.id,
                    "title": survey.title,
                    "description": survey.description,
                    "share_token": survey.share_token
                }
                for survey in surveys
            ]
        )

    except PermissionError as e:
        return error_response(message=str(e), status_code=403)

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/<int:survey_id>", methods=["GET"])
@jwt_required()
def get_single_survey(survey_id):

    try:
        creator_id = get_current_creator_id()

        survey = get_survey(
            survey_id,
            creator_id
        )

        return success_response(
            message="Survey retrieved successfully.",
            data={
                "id": survey.id,
                "title": survey.title,
                "description": survey.description,
                "share_token": survey.share_token,
                "questions": [
                    {
                        "id": question.id,
                        "question": question.question_text,
                        "question_type": question.question_type,
                        "required": question.required,
                        "options": [
                            option.option_text
                            for option in question.options
                        ]
                    }
                    for question in survey.questions
                ]
            }
        )

    except PermissionError as e:
        return error_response(message=str(e), status_code=403)

    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=404
        )

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )

@survey_bp.route("/<int:survey_id>", methods=["PUT"])
@jwt_required()
def update_existing_survey(survey_id):

    try:
        creator_id = get_current_creator_id()

        data = request.get_json()

        survey = update_survey(
            survey_id=survey_id,
            creator_id=creator_id,
            data=data
        )

        return success_response(
            message="Survey updated successfully.",
            data={
                "id": survey.id,
                "title": survey.title,
                "description": survey.description,

                "share_token": survey.share_token
            }
        )

    except PermissionError as e:
        return error_response(message=str(e), status_code=403)

    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=404
        )

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/<int:survey_id>", methods=["DELETE"])
@jwt_required()
def delete_existing_survey(survey_id):

    try:
        creator_id = get_current_creator_id()

        delete_survey(
            survey_id=survey_id,
            creator_id=creator_id
        )

        return success_response(
            message="Survey deleted successfully."
        )

    except PermissionError as e:
        return error_response(message=str(e), status_code=403)

    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=404
        )

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/<int:survey_id>/share/email", methods=["POST"])
@jwt_required()
def email_survey_invitation(survey_id):
    try:
        creator_id = get_current_creator_id()
        creator = db.session.get(User, creator_id)
        try:
            survey = get_survey(survey_id, creator_id)
        except ValueError as e:
            return error_response(message=str(e), status_code=404)

        data = request.get_json() or {}

        sent_count = send_survey_invitations(
            survey=survey,
            creator=creator,
            emails=data.get("emails"),
        )

        return success_response(
            message="Survey invitations sent successfully.",
            data={"sent_count": sent_count},
        )
    except PermissionError as e:
        return error_response(message=str(e), status_code=403)
    except ValueError as e:
        return error_response(message=str(e), status_code=400)
    except RuntimeError as e:
        return error_response(message=str(e), status_code=503)
    except Exception:
        return error_response(
            message="Unable to send survey invitations. Please try again later.",
            status_code=502,
        )


@survey_bp.route("/share/<string:share_token>", methods=["GET"])
def get_shared_survey_route(share_token):

    try:

        survey = get_shared_survey(share_token)

        return success_response(
            message="Survey retrieved successfully.",
            data={
                "title": survey.title,
                "description": survey.description,
                "questions": [
                    {
                        "id": q.id,
                        "question": q.question_text,
                        "question_type": q.question_type,
                        "required": q.required,
                        "options": [
                            option.option_text
                            for option in q.options
                        ]
                    }
                    for q in survey.questions
                ]
            }
        )

    except ValueError as e:

        return error_response(
            message=str(e),
            status_code=404
        )


@survey_bp.route("/share/<string:share_token>/responses", methods=["POST"])
@jwt_required()
def submit_survey_response(share_token):

    try:
        data = request.get_json()
        user_id = get_jwt_identity()

        response = submit_response(
            share_token=share_token,
            user_id=user_id,
            data=data
        )


        return success_response(
            message="Response submitted successfully.",
            data={
                "response_id": response.id
            },
            status_code=201
        )

    except ValueError as e:

        return error_response(
            message=str(e),
            status_code=404
        )

    except Exception as e:

        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/<int:survey_id>/analytics", methods=["GET"])
@jwt_required()
def get_survey_analytics(survey_id):

    try:
        user_id = get_current_creator_id()

        analytics = get_survey_analytics_service(
            survey_id=survey_id,
            user_id=user_id
        )

        return success_response(
            message="Survey analytics retrieved successfully.",
            data=analytics,
            status_code=200
        )

    except PermissionError as e:
        return error_response(
            message=str(e),
            status_code=403
        )

    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=404
        )

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )

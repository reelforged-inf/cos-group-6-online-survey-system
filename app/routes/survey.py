from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from gunicorn.config import User

from app.services.survey_service import (create_survey,  get_creator_surveys, get_survey, update_survey, delete_survey, get_shared_survey)
from app.services.response_service import submit_response
from app.services.analytics_service import get_survey_analytics_service
from app.utils.helpers import success_response, error_response


survey_bp = Blueprint(
    "survey",
    __name__,
    url_prefix="/api/surveys"
)


@survey_bp.route("", methods=["POST"])
@jwt_required()
def create():

    try:
        data = request.get_json()

        creator_id = int(get_jwt_identity())

        user = User.query.get(creator_id)

        if not user or user.role.lower() != "creator":
            return error_response(
                message="Only creators can create surveys.",
                status_code=403
            )

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

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/", methods=["GET"])
@jwt_required()
def get_surveys():

    try:
        creator_id = int(get_jwt_identity()) 
        

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

    except Exception as e:
        return error_response(
            message=str(e),
            status_code=400
        )


@survey_bp.route("/<int:survey_id>", methods=["GET"])
@jwt_required()
def get_single_survey(survey_id):

    try:
        creator_id = int(get_jwt_identity())
       
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
        creator_id = int(get_jwt_identity())

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
        creator_id = int(get_jwt_identity())

        delete_survey(
            survey_id=survey_id,
            creator_id=creator_id
        )

        return success_response(
            message="Survey deleted successfully."
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
@jwt_required(optional=True)
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
        user_id = get_jwt_identity()

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

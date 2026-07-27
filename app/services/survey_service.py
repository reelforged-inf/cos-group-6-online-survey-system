import secrets

from app.extensions import db
from app.models import Survey, Question, Option


def create_survey(data, creator_id):
    """
    Creates a survey together with all its questions and options
    in a single database transaction.

    Args:
        data (dict): Survey payload from the frontend.
        creator_id (int): Authenticated user's ID.

    Returns:
        Survey: Newly created survey object.
    """

    try:
        # Generate unique share token
        share_token = secrets.token_urlsafe(16)

        # Create survey
        survey = Survey(
            title=data["title"],
            description=data.get("description"),
            share_token=share_token,
            creator_id=creator_id
        )

        db.session.add(survey)

        # Get survey.id before commit
        db.session.flush()

        # Create questions
        for index, question_data in enumerate(data.get("questions", []), start=1):

            question = Question(
                survey_id=survey.id,
                question_text=question_data["question"],
                question_type=question_data["question_type"],
                required=question_data.get("required", False),
                order=index
            )

            db.session.add(question)

            # Get question.id for options
            db.session.flush()

            # Create options (if any)
            for option_text in question_data.get("options", []):

                option = Option(
                    question_id=question.id,
                    option_text=option_text
                )

                db.session.add(option)

        # Save everything permanently
        db.session.commit()

        return survey

    except Exception as e:
        db.session.rollback()
        raise e


def get_creator_surveys(creator_id):
    """
    Returns all surveys created by the authenticated creator.
    """

    surveys = (
        Survey.query
        .filter_by(creator_id=creator_id)
        .order_by(Survey.created_at.desc())
        .all()
    )

    return surveys    


def get_survey(survey_id, creator_id):

    """
    Return a single survey belonging to the authenticated creator.
    """

    survey = Survey.query.filter_by(
        id=survey_id,
        creator_id=creator_id
    ).first()

    if not survey:
        raise ValueError("Survey not found.")

    return survey


def update_survey(survey_id, creator_id, data):
    """
    Update an existing survey together with all questions and options.
    """

    survey = Survey.query.filter_by(
        id=survey_id,
        creator_id=creator_id
    ).first()

    if not survey:
        raise ValueError("Survey not found.")

    try:
        # Update survey details
        survey.title = data["title"]
        survey.description = data.get("description")

        # Remove existing questions.
        # Because of cascade="all, delete-orphan",
        # options are removed automatically.
        survey.questions.clear()

        db.session.flush()

        # Recreate questions
        for index, question_data in enumerate(data.get("questions", []), start=1):

            question = Question(
                survey=survey,
                question_text=question_data["question"],
                question_type=question_data["question_type"],
                required=question_data.get("required", False),
                order=index
            )

            db.session.add(question)
            db.session.flush()

            for option_text in question_data.get("options", []):

                option = Option(
                    question=question,
                    option_text=option_text
                )

                db.session.add(option)

        db.session.commit()

        return survey

    except Exception:
        db.session.rollback()
        raise


def delete_survey(survey_id, creator_id):
    """
    Delete a survey belonging to the authenticated creator.
    """

    survey = Survey.query.filter_by(
        id=survey_id,
        creator_id=creator_id
    ).first()

    if not survey:
        raise ValueError("Survey not found.")

    try:
        db.session.delete(survey)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise


def get_shared_survey(share_token):

    survey = Survey.query.filter_by(
        share_token=share_token,
       
    ).first()

    if not survey:
        raise ValueError("Survey not found.")

    return survey

from app.extensions import db
from app.models import Survey, Response, Answer, User, UserRole


def submit_response(share_token, user_id, data):
    """
    Save a respondent's submission for a survey.
    """

    # Find the survey
    survey = Survey.query.filter_by(
        share_token=share_token
    ).first()

    if not survey:
        raise ValueError("Survey not found.")

    user = User.query.get(user_id)

    if not user:
        raise ValueError("User not found.")

    if user.role != UserRole.RESPONDENT:
        raise PermissionError(
        "Only respondents can submit surveys."
    )

    responses = data.get("responses", [])

    if not responses:
        raise ValueError("No responses were submitted.")

    # Build lookup of survey questions
    questions = {
        question.id: question
        for question in survey.questions
    }

    # Prevent duplicate question submissions
    seen = set()

    # Store submitted answers for required-field validation
    submitted = {}

    # Validate submitted answers
    for item in responses:

        question_id = item.get("question_id")
        answer = item.get("answer")

        if question_id is None:
            raise ValueError("question_id is required.")

        if question_id in seen:
            raise ValueError(
                f"Duplicate answer submitted for question {question_id}."
            )

        seen.add(question_id)

        question = questions.get(question_id)

        if not question:
            raise ValueError(
                f"Question {question_id} does not belong to this survey."
            )

        submitted[question_id] = answer

        # Required question cannot be empty
        if question.required:
            if answer is None or str(answer).strip() == "":
                raise ValueError(
                    f'"{question.question_text}" is required.'
                )

        # Validate multiple choice & dropdown
        if question.question_type in [
            "multiple_choice",
            "dropdown"
        ]:

            allowed = [
                option.option_text
                for option in question.options
            ]

            if answer not in allowed:
                raise ValueError(
                    f'Invalid answer for "{question.question_text}".'
                )

        # Validate checkbox
        elif question.question_type == "checkbox":

            if not isinstance(answer, list):
                raise ValueError(
                    f'"{question.question_text}" must be a list.'
                )

            allowed = {
                option.option_text
                for option in question.options
            }

            if not set(answer).issubset(allowed):
                raise ValueError(
                    f'Invalid option selected for "{question.question_text}".'
                )

    # Ensure every required question was answered
    for question in survey.questions:

        if question.required and question.id not in submitted:
            raise ValueError(
                f'"{question.question_text}" is required.'
            )

    # Prevent duplicate survey submissions
    existing_response = Response.query.filter_by(
        survey_id=survey.id,
        user_id=user_id
    ).first()

    if existing_response:
        raise ValueError(
            "You have already submitted this survey."
        )

    try:

        # Create response
        response = Response(
            survey_id=survey.id,
            user_id=user_id
        )

        db.session.add(response)
        db.session.flush()

        # Save answers
        for item in responses:

            answer = Answer(
                response_id=response.id,
                question_id=item["question_id"],
                answer_text=item["answer"]
            )

            db.session.add(answer)

        db.session.commit()

        return response

    except Exception:
        db.session.rollback()
        raise
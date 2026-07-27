from app.extensions import db
from app.models import Survey, User, UserRole, Answer


def get_survey_analytics_service(survey_id, user_id):
    """
    Retrieve analytics for a survey owned by the creator.
    """

    # Find user
    user = db.session.get(User, user_id)

    if not user:
        raise ValueError("User not found.")

    # Only creators can view analytics
    if user.role != UserRole.CREATOR:
        raise PermissionError(
            "Only creators can view survey analytics."
        )

    # Find survey
    survey = db.session.get(Survey, survey_id)

    if not survey:
        raise ValueError("Survey not found.")

    # Ensure ownership
    if survey.creator_id != user.id:
        raise PermissionError(
            "You do not have permission to view this survey."
        )

    # Total survey responses
    total_responses = len(survey.responses)

    questions_data = []

    # Analyze each question
    for question in survey.questions:

        question_summary = {
            "question_id": question.id,
            "question": question.question_text,
            "type": question.question_type,
        }

        # ==============================
        # Multiple Choice / Dropdown
        # ==============================
        if question.question_type in [
            "multiple_choice",
            "dropdown"
        ]:

            results = []

            for option in question.options:

                count = Answer.query.filter_by(
                    question_id=question.id,
                    answer_text=option.option_text
                ).count()

                percentage = (
                    (count / total_responses) * 100
                    if total_responses > 0
                    else 0
                )

                results.append({
                    "option": option.option_text,
                    "count": count,
                    "percentage": round(percentage, 2)
                })

            question_summary["results"] = results

        # ==============================
        # Short Answer / Paragraph
        # ==============================
        elif question.question_type in [
            "short_answer",
            "paragraph",
            "text"
        ]:

            answers = Answer.query.filter_by(
                question_id=question.id
            ).all()

            question_summary["responses"] = [
                answer.answer_text
                for answer in answers
            ]

        # ==============================
        # Checkbox
        # ==============================
        elif question.question_type == "checkbox":

            results = []

            answers = Answer.query.filter_by(
                question_id=question.id
            ).all()

            for option in question.options:

                count = 0

                for answer in answers:

                    if (
                        answer.answer_text
                        and option.option_text in answer.answer_text
                    ):
                        count += 1

                percentage = (
                    (count / total_responses) * 100
                    if total_responses > 0
                    else 0
                )

                results.append({
                    "option": option.option_text,
                    "count": count,
                    "percentage": round(percentage, 2)
                })

            question_summary["results"] = results

        questions_data.append(question_summary)

    return {
        "survey": {
            "id": survey.id,
            "title": survey.title,
            "description": survey.description,
        },
        "total_responses": total_responses,
        "questions": questions_data,
    }
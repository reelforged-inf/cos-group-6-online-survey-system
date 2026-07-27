from app.extensions import db
from datetime import datetime


class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)

    survey_id = db.Column(
        db.Integer,
        db.ForeignKey("surveys.id"),
        nullable=False
    )

    submitted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    survey = db.relationship(
        "Survey",
        back_populates="responses"
    )

    answers = db.relationship(
        "Answer",
        back_populates="response",
        cascade="all, delete-orphan"
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("users.id"),
    nullable=False
    )

    respondent = db.relationship(
    "User",
    back_populates="responses"
    )
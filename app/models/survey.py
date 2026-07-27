from datetime import datetime
from app.extensions import db


class Survey(db.Model):
    __tablename__ = "surveys"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Survey Information
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Unique link for sharing
    share_token = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    # Owner of the survey
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Relationship back to the owner
    creator = db.relationship(
    "User",
    back_populates="surveys"
    )

    # Creation time
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships with Questions and Responses
    questions = db.relationship(
        "Question",
        back_populates="survey",
        cascade="all, delete-orphan",
        lazy=True
    )


    responses = db.relationship(
    "Response",
    back_populates="survey",
    cascade="all, delete-orphan"
)
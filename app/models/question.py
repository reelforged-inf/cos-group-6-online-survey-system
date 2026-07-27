from app.extensions import db

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)

    survey_id = db.Column(
        db.Integer,
        db.ForeignKey("surveys.id"),
        nullable=False
    )

    question_text = db.Column(
        db.Text,
        nullable=False
    )

    question_type = db.Column(
        db.String(50),
        nullable=False
    )

    required = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    order = db.Column(
        db.Integer,
        nullable=False
    )

    survey = db.relationship(
    "Survey",
    back_populates="questions"
    )


    options = db.relationship(
        "Option",
        back_populates="question",
        cascade="all, delete-orphan",
        lazy=True
    )

    answers = db.relationship(
    "Answer",
    back_populates="question",
    cascade="all, delete-orphan"
)
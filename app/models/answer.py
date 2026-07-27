from app.extensions import db


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)

    response_id = db.Column(
        db.Integer,
        db.ForeignKey("responses.id"),
        nullable=False
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False
    )

    answer_text = db.Column(
        db.Text,
        nullable=False
    )

    response = db.relationship(
        "Response",
        back_populates="answers"
    )

    question = db.relationship(
        "Question",
        back_populates="answers"
    )
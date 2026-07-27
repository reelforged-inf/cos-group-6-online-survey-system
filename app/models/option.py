from app.extensions import db


class Option(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)

    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id"),
        nullable=False
    )

    option_text = db.Column(
        db.String(255),
        nullable=False
    )

    question = db.relationship(
    "Question",
    back_populates="options"
)
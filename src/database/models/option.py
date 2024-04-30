from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import Question
from src.database import db
import sqlalchemy


class Option(db.Model):
    __tablename__ = 'options'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    question_id = mapped_column(sqlalchemy.ForeignKey('questions.id'), index=True)
    content: Mapped[str] = mapped_column(sqlalchemy.String(128), nullable=False)
    score: Mapped[float] = mapped_column(sqlalchemy.Float, nullable=False)
    question: Mapped[Question] = relationship('Question', back_populates='options')
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)
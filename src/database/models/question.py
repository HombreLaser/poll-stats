from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import Form
from src.database import db
import sqlalchemy
import typing


Type = typing.Literal['open', 'selection', 'confirmation']


class Question(db.Model):
    __tablename__ = 'questions'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    form_id = mapped_column(sqlalchemy.ForeignKey('forms.id'), index=True)
    type: Mapped[Type] = mapped_column(
        sqlalchemy.Enum('open', 'selection', 'radio', name='type')
    )
    content: Mapped[str] = mapped_column(sqlalchemy.String(256), nullable=False)
    # Para ser usado en preguntas de radio button. (Confirmación)
    score: Mapped[float] = mapped_column(sqlalchemy.Float, nullable=True)
    # Si es de selección, contará con una lista JSON que describirá las opciones
    # Estructura:
    # [{ 'content': 'respuesta', 'score': 'ponderación' }]
    options = relationship('Option', back_populates='question', lazy='select',
                                     cascade='save-update,merge,delete,delete-orphan')
    form: Mapped[Form] = relationship('Form', back_populates='questions') 
    required: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)
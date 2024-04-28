from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import UserAccount
from src.database import db
import sqlalchemy
import typing

# Review: estado por defecto. No se ha generado un share_key, y por ende, no es público.
# Open: el formulario está actualmente recibiendo respuestas.
# Closed: el formulario está cerrado y ya recibió todas las respuestas.
Status = typing.Literal['review', 'open', 'closed']


class Form(db.Model):
    __tablename__ = 'forms'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    user_account_id = mapped_column(sqlalchemy.ForeignKey('user_accounts.id'), index=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(512), nullable=False)
    status: Mapped[Status] = mapped_column(
        sqlalchemy.Enum('review', 'open', 'closed', name='status')
    )
    public_key: Mapped[str] = mapped_column(sqlalchemy.String(24), nullable=True, index=True)
    author: Mapped[UserAccount] = relationship('UserAccount', back_populates='forms')
    questions = relationship('Question', back_populates='form', lazy='select', 
                                         cascade='save-update,merge,delete,delete-orphan')
    responses = relationship('Response', back_populates='form', lazy='select', 
                                         cascade='save-update,merge,delete,delete-orphan')
    created_at = mapped_column(sqlalchemy.DateTime) 
    updated_at = mapped_column(sqlalchemy.DateTime)

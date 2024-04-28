from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models import Form
from src.database import db
import sqlalchemy


class Response(db.Model):
    __tablename__ = 'responses'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    form_id = mapped_column(sqlalchemy.ForeignKey('forms.id'), index=True)
    data: Mapped[list[dict[str, any]]] = mapped_column(sqlalchemy.JSON, nullable=False)
    form: Mapped[Form] = relationship('Form', back_populates='responses')
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)
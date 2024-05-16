from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from src.database.models import UserAccount
from src.database import db
import sqlalchemy
import typing


Type = typing.Literal['csv', 'sqlite']
Status = typing.Literal['pending', 'in_process', 'done']


class Export(db.Model):
    __tablename__ = 'exports'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    owner_id = mapped_column(sqlalchemy.ForeignKey('user_accounts.id'),
                             nullable=False, index=True)
    type: Mapped[Type] = mapped_column(
        sqlalchemy.Enum('csv', 'sqlite', name='type')
    )
    status: Mapped[Status] = mapped_column(
        sqlalchemy.Enum('pending', 'in_process', 'done', name='status')
    )
    file = mapped_column(FileField)
    owner: Mapped[UserAccount] = relationship('UserAccount',
                                              back_populates='exports')
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)

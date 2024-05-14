from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_file import FileField
from sqlalchemy_file.validators import ContentTypeValidator
from src.database.models import UserAccount
from src.database import db
import sqlalchemy


class InterpreterUpload(db.Model):
    __tablename__ = 'interpreter_uploads'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    owner_id = mapped_column(sqlalchemy.ForeignKey('user_accounts.id'),
                             nullable=False, index=True)
    file = mapped_column(FileField(validators=[ContentTypeValidator(
        allowed_content_types=['application/octet-stream'])]))
    owner: Mapped[UserAccount] = relationship('UserAccount',
                                              back_populates='exports')
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)

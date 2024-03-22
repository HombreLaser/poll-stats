import sqlalchemy
from sqlalchemy.orm import mapped_column
from src.database import db


class UserAccount(db.Model):
    __tablename__ = 'user_accounts'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    email = mapped_column(sqlalchemy.String(256), nullable=False)
    role = mapped_column(sqlalchemy.String(12), default='administrator')
    first_name = mapped_column(sqlalchemy.String(64), nullable=False)
    last_name = mapped_column(sqlalchemy.String(64), nullable=False)
    activated = mapped_column(sqlalchemy.Boolean, default=False)
    # Nullable porque será definido por el usuario cuando acceda a la invitación.
    password = mapped_column(sqlalchemy.String(256), nullable=True) 
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)

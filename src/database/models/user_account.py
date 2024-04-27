import sqlalchemy
import scrypt
import typing
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.database import db


class UserAccount(db.Model):
    __tablename__ = 'user_accounts'

    id = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(sqlalchemy.String(256), nullable=False, unique=True)
    role = mapped_column(sqlalchemy.String(16), default='administrator')
    first_name: Mapped[str] = mapped_column(sqlalchemy.String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(sqlalchemy.String(64), nullable=False)
    invite_code = mapped_column(sqlalchemy.String(128), nullable=True)
    activated: Mapped[str] = mapped_column(sqlalchemy.Boolean, default=False)
    # Nullable porque será definido por el usuario cuando acceda a la invitación.
    _password = mapped_column('password', sqlalchemy.String(512), nullable=True)
    forms = relationship('Form', back_populates='author')
    created_at = mapped_column(sqlalchemy.DateTime)
    updated_at = mapped_column(sqlalchemy.DateTime)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = scrypt.encrypt(current_app.config['SECRET_KEY'], password, maxtime=0.5).hex()

    def verify_password(self, guessed_password):
        try:
            scrypt.decrypt(bytes.fromhex(self._password), guessed_password, maxtime=0.8)
            return True
        except scrypt.error:
            return False

from multiprocessing import Process
import sqlalchemy as sa
from src.database.models import Export, UserAccount
from src.database import db


def export_to_sqlite(export_id):
    export = db.session.get(Export, export_id)


def begin_export_to_sqlite(user_account_id):
    user = db.session.get(UserAccount, user_account_id)
    export = Export(owner=user, status='pending', type='sqlite')
    db.session.add(export)
    db.session.commit()

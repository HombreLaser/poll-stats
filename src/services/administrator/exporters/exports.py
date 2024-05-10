from multiprocessing import Process
import sqlalchemy as sa
from src.services.administrator.exporters import SQLiteExporter
from src.database.models import Export, UserAccount
from src.database import db


def export_to_sqlite(export_id):
    exporter = SQLiteExporter(export_id)
    exporter.start()


def begin_export_to_sqlite(user_account_id):
    user = db.session.get(UserAccount, user_account_id)
    export = Export(owner=user, status='pending', type='sqlite')
    db.session.add(export)
    db.session.commit()
    job = Process(target=export_to_sqlite, args=(export.id,))
    job.start()
    job.join()

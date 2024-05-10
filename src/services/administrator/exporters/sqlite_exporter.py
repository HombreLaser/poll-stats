from src.database.models import Export
from src.database import db


class SQLiteExporter:
    def __init__(self, export_id: int):
        self._export = db.session.get(Export, export_id)
        self._user = self._export.owner

import sqlalchemy as sa
import sqlalchemy.orm as orm
import secrets
import sqlite3
from src.database.models import Export, Form, Response
from src.database import db


class SQLiteExporter:
    def __init__(self, export_id: int):
        self._export = db.session.get(Export, export_id)
        self._forms = self._get_user_forms()
        self._sqlite = sqlite3.connect(f"./tmp/{secrets.token_hex(12)}.db")
        self._sqlite_cursor = self._sqlite.cursor()
        self._init_database()
        self._sqlite.close()

    def start(self):
        print(self._export.id)

    def _get_user_forms(self):
        query = sa.select(Form) \
                  .options(orm.joinedload(Form.responses)) \
                  .filter(Form.user_account_id == self._export.owner_id)

        return db.session.execute(query).scalars()

    def _init_database(self):
        create_table_forms = ('CREATE TABLE forms(id INTEGER PRIMARY KEY '
                              'AUTOINCREMENT, name TEXT NOT NULL)')
        create_table_questions = ('CREATE TABLE questions(id INTEGER PRIMARY '
                                  'KEY AUTOINCREMENT, content TEXT NOT NULL, '
                                  'form_id INTEGER, type TEXT NOT NULL, '
                                  'FOREIGN KEY(form_id) REFERENCES forms(id))')
        create_table_responses = ('CREATE TABLE responses(id INTEGER PRIMARY '
                                  'KEY AUTOINCREMENT, question_id INTEGER, '
                                  'content TEXT NOT NULL, score FLOAT, '
                                  'FOREIGN KEY(question_id) REFERENCES '
                                  'questions(id))')
        self._sqlite_cursor.execute(create_table_forms)
        self._sqlite_cursor.execute(create_table_questions)
        self._sqlite_cursor.execute(create_table_responses)

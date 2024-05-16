import sqlalchemy as sa
import sqlalchemy.orm as orm
import secrets
import sqlite3
from pathlib import Path
from src.database.models import Export, Form, Response
from src.database import db


class SQLiteExporter:
    def __init__(self, export_id: int):
        self._export = db.session.get(Export, export_id)
        self._export.status = 'in_process'
        db.session.commit()
        self._database_file_path = f"./tmp/{secrets.token_hex(12)}.db"
        self._sqlite = sqlite3.connect(self._database_file_path)
        self._sqlite_cursor = self._sqlite.cursor()

    def start(self):
        self._init_database()
        self._insert_forms()
        self._insert_responses()
        self._sqlite.close()
        self._upload_db_file()
        self._export.status = 'done'
        db.session.commit()

    def _init_database(self):
        create_table_forms = ('CREATE TABLE forms(id INTEGER PRIMARY KEY, '
                              ' name TEXT NOT NULL)')
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

    def _insert_forms(self):
        forms_to_insert = []

        for form in self._forms():
            forms_to_insert.append((form.id, form.name))

        self._sqlite_cursor.executemany(
            'INSERT INTO forms (id, name) VALUES(?, ?)',
            forms_to_insert
        )
        self._sqlite.commit()

    def _insert_responses(self):
        for response in self._responses():
            for response_data in response.data:
                question_id = self._sqlite_cursor.execute(
                    'SELECT id FROM questions WHERE content = ?',
                    (response_data['question'],)).fetchone()

                if question_id is None:
                    question_id = self._insert_question(response_data,
                                                        response.id)

                self._insert_response(response_data, question_id[0])

    def _insert_response(self, response_data: dict, question_id: int):
        operation = 'INSERT INTO responses (question_id, content'

        if self._response_is_selection_type(response_data):
            self._sqlite_cursor \
                .execute(operation + ', score) VALUES(?, ?, ?)',
                         (question_id,
                          response_data['response']['response'],
                          response_data['response']['score']))
        else:
            self._sqlite_cursor \
                .execute(operation + ') VALUES(?, ?)',
                         (question_id,
                          response_data['response']))

        self._sqlite.commit()

    def _insert_question(self, response_data: dict, form_id: int):
        if self._response_is_selection_type(response_data):
            question_type = 'selection'
        else:
            question_type = 'open'

        sql_string = ('INSERT INTO questions (content, type, form_id)'
                      'VALUES (?, ?, ?)')
        self._sqlite_cursor.execute(sql_string, (response_data['question'],
                                                 question_type, form_id))
        self._sqlite.commit()

        return self._sqlite_cursor.execute(
            'SELECT id FROM questions ORDER BY id desc LIMIT 1').fetchone()

    def _response_is_selection_type(self, response_data: dict):
        return isinstance(response_data['response'], dict)

    def _responses(self):
        query = sa.select(Form.id, Response.data) \
                  .join(Response.form) \
                  .filter(Form.user_account_id == self._export.owner_id)

        return db.session.execute(query)

    def _forms(self):
        query = sa.select(Form.id, Form.name) \
                  .filter(Form.user_account_id == self._export.owner_id)

        return db.session.execute(query)

    def _upload_db_file(self):
        with open(self._database_file_path, 'rb') as database_file:
            self._export.file = database_file
            db.session.commit()

        file = Path(self._database_file_path)
        file.unlink()

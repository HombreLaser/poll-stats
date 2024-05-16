import sqlite3
from src.database import db
from src.database.models import UserAccount, InterpreterUpload


def create_upload(user_id, form):
    current_user = db.session.get(UserAccount, user_id)
    upload = InterpreterUpload(owner=current_user,
                               name=form.database.data.filename)
    upload.file = form.database.data
    db.session.add(upload)
    db.session.commit()

    return upload


class SQLInterpreter:
    def __init__(self, upload, sql_sentence):
        self._upload = upload
        self._sql_sentence = sql_sentence

    def __enter__(self):
        self._connection = self._database_connection()
        self._cursor = self._connection.cursor()

        try:
            return self._cursor.execute(self._sql_sentence).fetchall(), None
        except sqlite3.OperationalError as error:
            return None, error

    def __exit__(self, exc_type, exc_value, traceback):
        self._connection.close()

    def _database_connection(self):
        return sqlite3.connect(self._upload.file['url'])

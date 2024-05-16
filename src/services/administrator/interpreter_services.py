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

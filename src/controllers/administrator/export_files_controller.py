import json
import sqlalchemy as sa
from flask import Blueprint, send_file
from pathlib import Path
from src.database import db
from src.lib import role_constraint


export_files_blueprint = Blueprint('export_files_controller', __name__)


@export_files_blueprint.get('/storage/exports/<file_id>')
@role_constraint('administrator')
def show(file_id: str):
    query = sa.text("SELECT * FROM exports WHERE JSON_VALUE(file, '$.file_id')"
                    '= :file_id')
    export = db.session.execute(query, {'file_id': file_id}).fetchone()
    db_path = Path(f".{json.loads(export.file)['url']}")

    return send_file(db_path, mimetype='application/octet-stream',
                     download_name=f"{file_id}.db")

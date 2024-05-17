import sqlalchemy as sa
import pandas as pd
import os
from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine
from src.database.models import Export, Form
from src.forms import CSVExportForm, choices
from src.database import db
from src.queries.administrator import ExportsQuery
from src.lib.constraints import role_constraint


csv_exports_blueprint = Blueprint('csv_exports_controller', __name__)
templates_context = f"views/administrator/csv_exports"


@csv_exports_blueprint.get('/administrator/exports/csv')
@role_constraint('administrator')
def index():
    query = ExportsQuery(request.args, session.get('user_id'))
    form = CSVExportForm()
    form.form_id.query = choices(session.get('user_id'))

    return render_template(f"{templates_context}/index.jinja",
                           exports=query.get_exports(),
                           form=form)


@csv_exports_blueprint.post('/administrator/exports/csv')
@role_constraint('administrator')
def create():
    form = CSVExportForm()
    form_id = int(request.form.get('form_id'))
    query = f'SELECT * FROM responses WHERE form_id = {form_id}'

    df = pd.read_sql(query, db.engine)

    try:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        if not os.path.exists(downloads_folder):
            os.makedirs(downloads_folder)

        df.to_csv(os.path.join(downloads_folder, "userForm2.csv"),
                  index=False, encoding='utf-8')
    except:
        print("Unable to access the Downloads folder. Saving the DataFrame without specific file path.")

        df.to_csv("userForm.csv", index=False)

        flash("Exportacion satisfactoria", "success")

    return redirect(url_for("csv_exports_controller.index"))

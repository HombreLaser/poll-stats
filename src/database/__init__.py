from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapper
from sqlalchemy import event, update


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def init_db(app):
    migrate = Migrate(app, db)
    db.init_app(app)


def clear_data(app):
    with app.app_context():
        meta = db.metadata
        if app.testing:
            for table in reversed(meta.sorted_tables):
                db.session.execute(table.delete())

            db.session.commit()


@event.listens_for(Mapper, 'after_insert')
def insert_created_and_updated_at_columns(mapper, connection, target):
    set_timestamps = (
        update(mapper.local_table).
        where(mapper.local_table.c.id == target.id).
        values(created_at=datetime.now(timezone.utc),
               updated_at=datetime.now(timezone.utc))
    )
    connection.execute(set_timestamps)



@event.listens_for(Mapper, 'before_update')
def set_updated_at_timestamp(mapper, connection, target):
    set_updated_at = (
        update(mapper.local_table).
        where(mapper.local_table.c.id == target.id).
        values(updated_at=datetime.now(timezone.utc))
    )
    connection.execute(set_updated_at)
import sqlalchemy as sa
from datetime import datetime, timedelta
from sqlalchemy import orm
from abc import ABC, abstractmethod
from src.queries import JoinedQueryBase
from src.database import db
from src.database.models import Response, Form


class ResponsesQuery(JoinedQueryBase):
    def __init__(self, params, user_id):
        super().__init__(params)
        self._user_id = user_id

    def get_responses(self):
        self._scope = sa.select(Response) \
                        .join(Response.form) \
                        .options(orm.contains_eager(Response.form)) \
                        .filter(Form.user_account_id == self._user_id)

        return self.search_joined_with(Response, Form, join=False)


class ResponseTimelapseQuery(ABC):
    def __init__(self, args):
        self._args = args
        self._user_role = self._args.get('user_role')
        self._user_id = self._args.get('user_id')

    def _responses_made(self, date: datetime):
        query = sa.select(sa.func.count()).select_from(Response) \
                                          .filter(
                                              Response.created_at >= date
                                          ).filter(Response.created_at < (
                                              date + self._timedelta()))
        query = self._scope(query)

        return db.session.execute(query).scalar()

    def _scope(self, query):
        if self._user_role == 'administrator':
            return query.join(Response.form).filter(
                Form.user_account_id == self._user_id)

        return query

    @abstractmethod
    def _timedelta(self):
        return timedelta()


class ResponsesOfTheYear(ResponseTimelapseQuery):
    pass


class ResponsesOfTheWeek(ResponseTimelapseQuery):
    def responses_count_by_day(self):
        counts = {}
        self._set_previous_seven_days()

        for date in self._dates:
            counts[date.strftime('%a')] = self._responses_made(date)

        return counts

    def _timedelta(self):
        return timedelta(days=1)

    def _set_previous_seven_days(self):
        self._dates = []

        for weekday in reversed(range(1, 8)):
            self._dates.append(datetime.now() - timedelta(days=weekday))

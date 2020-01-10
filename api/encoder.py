import datetime
import enum
import uuid

from connexion.apps.flask_app import FlaskJSONEncoder

from api.db.models import Base


class JSONEncoder(FlaskJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, (map, set, frozenset)):
            return list(o)
        elif isinstance(o, datetime.datetime):
            if o.tzinfo:
                # eg: '2015-09-25T23:14:42.588601+00:00'
                return o.isoformat('T')
            else:
                # No timezone present - assume UTC.
                # eg: '2015-09-25T23:14:42.588601Z'
                return o.isoformat('T') + 'Z'
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, enum.Enum):
            return o.name
        if isinstance(o, Base):
            return dict((col, getattr(o, col)) for col in o.__table__.columns.keys())
        return FlaskJSONEncoder.default(self, o)

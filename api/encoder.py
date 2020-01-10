import datetime
import enum
import uuid
from typing import Dict

from connexion.apps.flask_app import FlaskJSONEncoder
from sqlalchemy.orm import class_mapper

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
            return sqlalchemy_base_to_dict(o)

        return FlaskJSONEncoder.default(self, o)


def sqlalchemy_base_to_dict(instance: Base, founded_relations=None) -> Dict:
    if founded_relations is None:
        founded_relations = set()
    instance_dict = dict((col, getattr(instance, col)) for col in instance.__table__.columns.keys())
    mapper = class_mapper(instance.__class__)
    for name, relation in mapper.relationships.items():
        if relation not in founded_relations:
            founded_relations.add(relation)
            related_obj = getattr(instance, name)
            if related_obj is None:
                instance_dict[name] = None
            else:
                if relation.uselist:
                    instance_dict[name] = [sqlalchemy_base_to_dict(child, set(founded_relations)) for child in
                                           related_obj]
                else:
                    instance_dict[name] = sqlalchemy_base_to_dict(related_obj, founded_relations)
    return instance_dict

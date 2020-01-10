from flask import current_app
from api.db.models import Event


def get_events(offset: int = 0, limit: int = 0):  # noqa: E501
    """Get events

     # noqa: E501

    :param offset: 
    :type offset: int
    :param limit: 
    :type limit: int

    :rtype: List[object]
    """
    return current_app.scoped_session.query(Event).slice(offset, offset + limit).all()

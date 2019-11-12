import connexion
import six

from api.models.event import Event  # noqa: E501
from api import util


def get_events(offset, limit):  # noqa: E501
    """Get events

     # noqa: E501

    :param offset: 
    :type offset: int
    :param limit: 
    :type limit: int

    :rtype: List[Event]
    """
    return 'do some magic!'

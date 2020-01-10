import typing as t

from flask import current_app

from api.db.models import Sign


def create_sign(data: t.Dict):  # noqa: E501
    """Create sign

     # noqa: E501

    :param data:
    :type data: dict | bytes

    :rtype: None
    """
    sign = current_app.scoped_session.query(Sign).filter(Sign.name == data['name']).first()
    if sign is not None:
        for key, value in data.items():
            setattr(sign, key, value)
    else:
        sign = Sign(**data)
        current_app.scoped_session.add(sign)
    current_app.scoped_session.commit()
    return sign


def get_signs(offset: int = 0, limit: int = 20):  # noqa: E501
    """Get signs

     # noqa: E501


    :rtype: None
    """
    return current_app.scoped_session.query(Sign).slice(offset, offset + limit).all()


def remove_sign(sign_id: str):
    sign = current_app.scoped_session.query(Sign).filter(Sign.id == sign_id).one()
    current_app.scoped_session.delete(sign)
    current_app.scoped_session.commit()
    return 204
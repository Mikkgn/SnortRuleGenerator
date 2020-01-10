import typing as t

from flask import current_app
from sqlalchemy.orm.exc import NoResultFound


def shutdown_session(response_or_exc):
    current_app.scoped_session.remove()
    return response_or_exc


def internal_server_error(exception: Exception) -> t.Tuple[str, int]:
    current_app.logger.exception(exception)
    return "Произошла непредвиденная ошибка", 500


def no_result_found(exception: NoResultFound) -> t.Tuple[str, int]:
    return "Объект не найден", 404

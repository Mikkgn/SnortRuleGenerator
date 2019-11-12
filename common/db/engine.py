import logging
import time
from typing import Dict

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy_utils import database_exists, create_database

logger = logging.getLogger(__name__)


def wait_db(db_host: str, db_name: str, db_user: str, db_pass: str, attemps: int = 10, pause: int = 10) -> None:
    logger.info(
        f'Проверка доступности БД по адресу {db_host}. '
        f'Время ожидания: {attemps * pause}с'
    )
    while attemps > 0:
        try:
            conn = Connection(engine=create_engine(get_database_conn_url(db_host, db_name, db_user, db_pass)),
                              # type: ignore
                              )
            conn.close()
        except OperationalError as exc:
            if 'does not exist' in str(exc):
                return
            attemps -= 1
            time.sleep(pause)
        except Exception as exc:
            logger.exception(
                f'Не удалось установить соединение с БД. {exc}'
                f'Осталось попыток: {attemps}'
            )
            attemps -= 1
            time.sleep(pause)
        else:
            logger.info('Соединение с БД установлено.')
            return
    logger.error('Не установлено соединение с БД')
    exit(1)


def init_db(config: Dict) -> None:
    url = get_database_conn_url(**config)
    if not database_exists(url):
        create_database(url)

    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', 'analyzer/db/migrations')
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        logger.exception(e)
        raise e
    logger.info('Миграции выполнены')


def get_database_conn_url(db_host: str, db_name: str, db_user: str, db_pass: str):
    return f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"


def create_scoped_session(db_configuration: Dict) -> Session:
    engine = create_engine(get_database_conn_url(**db_configuration))

    return scoped_session(sessionmaker(bind=engine))

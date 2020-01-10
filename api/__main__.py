#!/usr/bin/env python3
import logging

import connexion
from sqlalchemy.orm.exc import NoResultFound

from api import encoder
from api.analyzer_status_handlers import AnalyzerStatusHandler
from api.config import configuration
from api.events_handler import EventsHandler
from api.middleware import no_result_found, internal_server_error, shutdown_session
from common.amqp_publisher import AMQPPublisher
from common.db.engine import create_scoped_session, init_db, wait_db

logger = logging.getLogger(__name__)


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    wait_db(**configuration['db_config'])
    init_db(configuration['db_config'], 'api')
    status_handler = AnalyzerStatusHandler(**configuration['rabbitmq_config'],
                                           scoped_session=create_scoped_session(configuration['db_config']))
    status_handler.start()
    events_handler = EventsHandler(**configuration['rabbitmq_config'],
                                   scoped_session=create_scoped_session(configuration['db_config']))
    events_handler.start()
    app.app.json_encoder = encoder.JSONEncoder
    app.app.amqp_publisher = AMQPPublisher(**configuration['rabbitmq_config'])
    app.app.scoped_session = create_scoped_session(configuration['db_config'])
    app.app.register_error_handler(NoResultFound, no_result_found)
    app.app.teardown_appcontext(shutdown_session)
    app.app.register_error_handler(Exception, internal_server_error)
    app.add_api('swagger.yaml', arguments={'title': 'Snort Rule Generator Api'}, pythonic_params=True)
    app.run(port=8080)
    status_handler.join()
    events_handler.join()
    logger.info('end')


if __name__ == '__main__':
    main()

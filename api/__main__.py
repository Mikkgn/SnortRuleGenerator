#!/usr/bin/env python3

import connexion
from sqlalchemy.orm.exc import NoResultFound

from api import encoder
from api.config import configuration
from api.middleware import no_result_found, internal_server_error, shutdown_session
from common.amqp_publisher import AMQPPublisher
from common.db.engine import create_scoped_session, init_db, wait_db


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    wait_db(**configuration['db_config'])
    init_db(configuration['db_config'], 'api')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.amqp_publisher = AMQPPublisher(**configuration['rabbitmq_config'])
    app.app.scoped_session = create_scoped_session(configuration['db_config'])
    app.app.register_error_handler(NoResultFound, no_result_found)
    app.app.teardown_appcontext(shutdown_session)
    app.app.register_error_handler(Exception, internal_server_error)
    app.add_api('swagger.yaml', arguments={'title': 'Snort Rule Generator Api'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()

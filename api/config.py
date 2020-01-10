import os

configuration = {
    "db_config": {
        'db_host': os.environ.get('DB_HOST', 'db'),
        'db_user': os.environ.get('DB_USER', 'root'),
        'db_pass': os.environ.get('DB_PASS', 'P@ssw0rd'),
        'db_name': 'api',
    },
    "rabbitmq_config": {
        'host': os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
        'user': os.environ.get('RABBIMTQ_USER', 'root'),
        'password': os.environ.get('RABBITMQ_PASSWORD', 'P@ssword')
    },
    "cache_limit": 50,
}

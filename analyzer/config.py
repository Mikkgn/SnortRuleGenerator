import os

configuration = {
    "rabbitmq_config": {
        'host': os.environ.get('RABBITMQ_HOST', '192.168.99.100`'),
        'user': os.environ.get('RABBIMTQ_USER', 'root'),
        'password': os.environ.get('RABBITMQ_PASS', 'P@ssword')
    },
    "cache_limit": 50,
}
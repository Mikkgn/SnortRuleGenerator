import os

configuration = {
    "rabbitmq_config": {
        'host': os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
        'user': os.environ.get('RABBIMTQ_USER', 'root'),
        'password': os.environ.get('RABBITMQ_PASSWORD', 'P@ssword'),
    },
    "event_exchange": {
        "exchange_name": "attack_event",
        "routing_key": "attack.detected",
        "queue": 'generate_rule'
    }
}

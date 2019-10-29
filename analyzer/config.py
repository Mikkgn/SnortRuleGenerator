import os

configuration = {
    "db_config": {
        'db_host': os.environ.get('DB_HOST', 'localhost'),
        'db_user': os.environ.get('DB_USER', 'root'),
        'db_pass': os.environ.get('DB_PASS', 'P@ssw0rd'),
        'db_name': 'analyzer',
    }
}
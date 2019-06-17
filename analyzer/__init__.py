import logging.config
import os
import yaml

with open(f'{os.path.dirname(__file__)}/logging_config.yaml', 'r') as file:
    logging.config.dictConfig(yaml.load(file.read(), Loader=yaml.FullLoader))

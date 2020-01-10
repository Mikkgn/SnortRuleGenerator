import logging

from rule_generator.config import configuration
from rule_generator.creator import RuleCreator

logger = logging.getLogger(__name__)

def main():
    logger.info(f"Starting {__name__}")
    creator = RuleCreator(configuration['rabbitmq_config'], configuration['event_exchange'])
    creator.start()
    creator.join()


main()

import config_reader
from KafkaDataWriter import DataWriterToKafkaTopic


NUMBER_OF_MESSAGES = int(config_reader.cfg.get('LAB', 'number_of_messages'))
ENCODING = config_reader.cfg.get('LAB', 'encoding')
MESSAGES_PER_FETCH = int(config_reader.cfg.get('LAB', 'messages_per_fetch'))


class StrategySelector(object):
    def __init__(self, url, filename):
        self.dataset_filename = filename.strip()
        self.dataset_url = url.strip()

        self.strategies = {
            'kafka': DataWriterToKafkaTopic(url=self.dataset_url, filename=self.dataset_filename)
        }

    def execute(self):
        strategy_name = config_reader.cfg.get('LAB', 'strategy_name')
        self.strategies[strategy_name].execute()



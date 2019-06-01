import pandas as pd
import json
import config_reader
from data_insertion_states import DataInsertionStates as States
from sodapy import Socrata
from kafka import KafkaProducer
from BaseDataWriter import  BaseDataWriter


NUMBER_OF_MESSAGES = int(config_reader.cfg.get('LAB', 'number_of_messages'))
ENCODING = config_reader.cfg.get('LAB', 'encoding')
MESSAGES_PER_FETCH = int(config_reader.cfg.get('LAB', 'messages_per_fetch'))


class DataWriterToKafkaTopic(BaseDataWriter):
    def __init__(self, url, filename):
        super(DataWriterToKafkaTopic, self).__init__(url, filename)

    def execute(self):
        dataset_id = '{}_{}'.format(self.dataset_url, self.dataset_filename)
        latest_status = self.redis_client.get(dataset_id)

        kafka_server = '{}:{}'.format(
            config_reader.cfg.get('LAB', 'kafka_host'),
            config_reader.cfg.get('LAB', 'kafka_port')
        )
        producer = KafkaProducer(
            bootstrap_servers=[kafka_server],
            value_serializer=lambda v: json.dumps(v).encode(ENCODING)
        )

        if latest_status == str(States.COMPLETED_STATUS) or latest_status == str(States.ATTEMPT_TO_REFILL_STATUS):
            self.redis_client.set(dataset_id, str(States.ATTEMPT_TO_REFILL_STATUS))

        client = Socrata(self.dataset_url, None)
        self.redis_client.set(dataset_id, str(States.STARTED_STATUS))

        for i in range(NUMBER_OF_MESSAGES):
            results = client.get(self.dataset_filename, limit=1, offset=i)
            results_df = pd.DataFrame.from_records(results)

            current_progress = 'row #{}'.format(str(i))

            self.redis_client.set(dataset_id, current_progress)
            producer.send(config_reader.cfg.get('LAB', 'elastic_search_topic'), results_df.to_dict())

            print("Results {}".format(current_progress))

        self.redis_client.set(dataset_id, str(States.COMPLETED_STATUS))

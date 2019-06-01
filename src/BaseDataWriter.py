import abc
import redis
import config_reader


class BaseDataWriter(metaclass=abc.ABCMeta):
    def __init__(self, url=None, filename=None):
        self.dataset_url = url
        self.dataset_filename = filename

        self.redis_client = redis.Redis(
            host=config_reader.cfg.get('LAB', 'redis_host'),
            port=int(config_reader.cfg.get('LAB', 'redis_port')),
            db=0
        )

    @abc.abstractmethod
    def execute(self):
        pass

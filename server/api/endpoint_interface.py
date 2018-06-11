from abc import ABCMeta, abstractmethod


class EndpointInterface(metaclass=ABCMeta):
    @property
    @abstractmethod
    def endpoint_url(self):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def insert_to_database(self):
        raise NotImplementedError


from abc import ABC, abstractmethod
from src.utilities.db_connection import MyDatabaseConnection

class BaseService(ABC):
    def __init__(self):
        self.dbcnx = MyDatabaseConnection()

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def create(self, model):
        pass

    @abstractmethod
    def update(self, model):
        pass

    @abstractmethod
    def delete(self, id):
        pass


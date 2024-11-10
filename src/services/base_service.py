
from abc import ABC, abstractmethod
from src.utilities.database import cnx


class BaseService(ABC):
    
    def __init__(self):
        self.dbcnx = cnx

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


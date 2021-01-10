from abc import ABCMeta, abstractmethod
from src.Models.TableData import TableData


class Diagram(object, metaclass=ABCMeta):
    def __init__(self, data: TableData):
        self.title = data.title
        self.cols = data.cols
        self.content = data.content

    @abstractmethod
    def display(self):
        pass

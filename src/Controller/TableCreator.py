from src.Models.TableData import TableData
from src.Views.Diagram.Table import Table


def create_table(data: TableData):
    Table(data).display()

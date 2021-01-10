import rich.table as rt
from rich.console import Console
from src.Models.TableData import TableData
from src.Utils.StringProcessor import str_process
from src.Views.Diagram.Diagram import Diagram


class Table(Diagram):
    def __init__(self, data: TableData):
        super().__init__(data)

    def display(self) -> None:
        """
        display the table on the console
        :return:
        """
        cols = tuple(map(str_process, self.cols))
        table = rt.Table(title=self.title, title_style="bold", header_style="#E4007F")
        for col in cols:
            table.add_column(col, style="#00FFFF")
        for row in self.content:
            row = tuple(map(lambda x: str(x), row))
            table.add_row(*row)
        console = Console()
        console.print(table)

import sys

sys.path.append("../..")
from src.Models.TableData import TableData
from src.Models.Workflow import tbd_work
from rich.console import Console
import rich.table as rt
from rich import box
from src.Utils.StringProcessor import str_process


class Table(object):
    def __init__(self, data: TableData):
        self.title = data.title
        self.cols = data.cols
        self.content = data.content


    @staticmethod
    def cols_process(cols: list) -> tuple:
        """
        transfer all col names in one cols
        :param cols: eg. [campaign_name, owner_full_name]
        :return: [Campaign Name, Owner Full Name]
        """
        return tuple(map(str_process, cols))

    def display(self) -> None:
        """
        display the table on the console
        :return:
        """
        cols = self.cols_process(self.cols)
        table = rt.Table(title=self.title, title_style="bold", header_style="#E4007F")
        for col in cols:
            table.add_column(col, style="#00FFFF")
        for row in self.content:
            row = tuple(map(lambda x: str(x), row))
            table.add_row(*row)
        console = Console()
        console.print(table)


if __name__ == '__main__':
    t = Table(tbd_work())
    t.display()

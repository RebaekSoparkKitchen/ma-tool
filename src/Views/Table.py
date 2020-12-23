import sys

sys.path.append("../..")
from src.Models.TableData import TableData
from src.Models.Workflow import tbd_work
from rich.console import Console
import rich.table as rt
from rich import box


class Table(object):
    def __init__(self, data: TableData):
        self.title = data.title
        self.cols = data.cols
        self.content = data.content

    @staticmethod
    def str_process(col_name: str) -> str:
        """
        transfer the lower case staff to the first capital words
        :param col_name: eg. campaign_name
        :return: eg. Campaign Name
        """
        if col_name == 'id':
            return col_name.upper()
        return col_name.replace('_', ' ').title()

    @staticmethod
    def cols_process(cols: list) -> tuple:
        """
        transfer all col names in one cols
        :param cols: eg. [campaign_name, owner_full_name]
        :return: [Campaign Name, Owner Full Name]
        """
        return tuple(map(Table.str_process, cols))

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

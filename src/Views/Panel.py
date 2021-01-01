import rich.panel as rp
from rich import print, box
from src.Models.TableData import TableData
from src.Utils.StringProcessor import str_process

class Panel(object):
    def __init__(self, data: TableData):
        self.title = data.title
        self.cols = data.cols
        self.content = data.content

    def display(self, dialogue=None, transfer_data=None):
        pk_id_index = self.cols.index('id')
        for item in self.content:
            info = ''
            for i in range(len(self.cols)):
                if item[i]:
                    info += f'[#E4007F]{str_process(self.cols[i])}:[/#E4007F] [#00FFFF]{item[i]}[/#00FFFF]'
                    if i != len(self.cols) - 1:
                        info += '\n'
            print(rp.Panel.fit(info, box=box.DOUBLE))
            # dialogue来自views, transfer_data来自于Model
            if transfer_data and dialogue:
                pk_id = item[pk_id_index]
                transfer_data(pk_id, dialogue())


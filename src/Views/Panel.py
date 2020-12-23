from rich import print, box
from src.Utils.StringProcessor import str_process
from src.Models.TableData import TableData
from src.Models.Workflow import campaign_id_work
import rich.panel as rp


class Panel(object):
    def __init__(self, data: TableData):
        self.title = data.title
        self.cols = data.cols
        self.content = data.content

    def display(self, dialogue=None, upload=None):
        for item in self.content:
            info = ''
            for i in range(len(self.cols)):
                info += f'[#E4007F]{self.cols[i]}:[/#E4007F] [#00FFFF]{item[i]}[/#00FFFF] \n'
                print(rp.Panel.fit(info, box=box.DOUBLE))
                # dialogue来自views, upload来自于Model
                dialogue()
                upload()




if __name__ == '__main__':
    print(campaign_id_work().cols)
    print(campaign_id_work().content)

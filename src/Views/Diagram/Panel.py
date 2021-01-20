import rich.panel as rp
from rich import print, box
from src.Models.TableData import TableData
from src.Utils.StringProcessor import str_process
from src.Views.Diagram.Diagram import Diagram


class Panel(Diagram):
    def __init__(self, data: TableData):
        super().__init__(data)

    def display(self):
        """
        Panel接收的数据是TableData，意味着它可能包含多行数据，然而panel一次只能打印一行数据，所以display实际上是提供一个生成器，每次用next调用，则会display下一行数据。
        :return:
        """
        for item in self.content:
            info = ''
            for i in range(len(self.cols)):
                info += f'[#E4007F]{str_process(self.cols[i])}:[/#E4007F] [#00FFFF]{item[i]}[/#00FFFF]'
                if i != len(self.cols) - 1:
                    info += '\n'
            yield print(rp.Panel.fit(info, box=box.DOUBLE))


if __name__ == '__main__':
    def f():
        a = [1,2,3]
        for i in a:
            yield print(i)
    a = f()
    a.__next__()
    a.__next__()
    a.__next__()

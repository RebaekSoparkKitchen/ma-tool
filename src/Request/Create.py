'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-11-24 11:23:07
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-25 23:49:46
@FilePath: \MA_tool\src\Request\Create.py
'''
import sys
sys.path.append("../..")
import datetime as dt
from src.Control.MA import MA
from src.Utils.Similarity import Similarity
from rich import print
from rich.panel import Panel
from rich.console import RenderGroup
from rich.prompt import Prompt, IntPrompt, Confirm
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion 
from src.Request.Key_bindings import short_cut


class Create(MA):
    def __init__(self):
        """
        docstring
        """
        super().__init__()
        self.name_list = self.sqlProcess("SELECT first_name, last_name FROM Staff")
        self.first_name = ''
        self.last_name = ''
        self.wave = 1
        self.blast_date = None
        self.event_date = None

    def search_name(self, input_name: str) -> list:
        """
        name: the input name
        """
        new_name = []
        for name in self.name_list:
            new_name.append([name, self.compare_name(name, input_name)])
    
        new_name.sort(key=lambda x: x[1], reverse=True)
        return new_name
    
    def compare_name(self, standard_name: tuple, input_name: str) -> float:
        """
        helper method
        standard name: ('Ivy', 'Tan')
        input name: 'Ivy Tan'
        """
        standard_full_name = standard_name[0] + ' ' + standard_name[1]
        return Similarity.compare(standard_full_name, input_name)

    def info(self, name: tuple):
        """
        return : department , location when input name
        """
        return self.sqlProcess(f"SELECT department, location FROM Staff WHERE first_name = '{name[0]}' AND last_name = '{name[1]}'")
    
    def name_dialogue(self) -> None:
        '''
        the conversation for name confirmation
        '''
        name_completer = WordCompleter(list(map(lambda x: ' '.join(x), c.name_list)), ignore_case=True, match_middle=True)
        name = prompt('请输入owner的名字', completer=name_completer, complete_while_typing=True, key_bindings=short_cut())
        for item in self.search_name(name):
            guess_name = item[0]
            
            print(Panel.fit('[green]' + guess_name[0] + ' ' + guess_name[1]+ '\n' +'[blue]' + self.info(guess_name)[0][0] + '\n' + '[blue]' + self.info(guess_name)[0][1]))
            
            command = Confirm.ask('您是指上面这个员工吗？', default=True)

            if command:
                self.first_name = guess_name[0]
                self.last_name = guess_name[1]
                self.department = self.info(guess_name)[0][0]
                self.location = self.info(guess_name)[0][1]
                break
        return
    
    def wave_dialogue(self):
        '''
        the conversation for the waves
        '''
        wave = IntPrompt.ask('这是第几波EDM？', default=1)
        self.wave = wave
        return

    @staticmethod
    def confirm_date(date1: dt.date, date2: dt.date, question: str):
        """
        helper method
        date1: input date
        date2: 待比较的date
        如果date1比date2小，就会触发问题
        """
        if date1 < date2:
            confirm = Confirm.ask(question)
            return confirm
        return True


    def blast_date_dialogue(self):
        '''
        main method
        let user input blast date
        '''
        while(True):
            date = Prompt.ask(f'请输入 [b]blast date[/b]')
            try:
                blast_date = dt.datetime.strptime(date,'%Y%m%d').date()
                if not Create.confirm_date(blast_date, dt.date.today(),'[#ffc107]您输入的blast date日期在今天之前，您确定吗？'):
                    continue
                self.blast_date = blast_date
                break
            except ValueError:
                print('[prompt.invalid]请输入正确的日期格式，eg: 20201125')
        return 

    def event_date_dialogue(self):

        '''
        main method
        let user input event date
        '''
        while(True):
            date = Prompt.ask(f'请输入 [b]event date[/b]')
            #如果blast date是空值，well，我还没想好怎么处理这个情况，先try except pass吧
            try:
                event_date = dt.datetime.strptime(date,'%Y%m%d').date()
                if not Create.confirm_date(event_date, dt.date.today(), '[#ffc107]此日期在今天之前，您确定吗'):
                    continue
                try:
                    event_date = dt.datetime.strptime(date,'%Y%m%d').date()
                    if not Create.confirm_date(event_date, self.blast_date, '[#ffc107]此日期在blast date之前，您确定吗'):
                        continue
                except TypeError:
                    pass
                    
                self.event_date = event_date
                break
            except ValueError:
                print('[prompt.invalid]请输入正确的日期格式，eg: 20201125')
        return 

    
        



if __name__ == "__main__":
    c = Create()
    
    # c.wave_dialogue()
    c.name_dialogue()
    # c.blast_date_dialogue()
    # c.event_date_dialogue()
    # print(c.first_name)
    # print(c.last_name)
    # print(c.department)
    # print(c.location)
    # print(c.blast_date)
    # print(c.event_date)
    # print(c.wave)

    
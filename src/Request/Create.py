'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-11-24 11:23:07
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-24 18:17:31
@FilePath: \MA_tool\src\Request\Create.py
'''
import sys
sys.path.append("../..")

from src.Control.MA import MA
from src.Utils.Similarity import Similarity
from rich import print
from rich.panel import Panel
from rich.console import RenderGroup
from rich.prompt import Prompt, IntPrompt

class Create(MA):
    def __init__(self):
        """
        docstring
        """
        super().__init__()
        self.name_list = self.sqlProcess("SELECT first_name, last_name FROM Staff")
        self.first_name = ''
        self.last_name = ''

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
        docstring
        """
        return self.sqlProcess(f"SELECT department, location FROM Staff WHERE first_name = '{name[0]}' AND last_name = '{name[1]}'")
    
    def name_conversation(self):
        '''
        the conversation for name confirmation
        '''
        name = input("请输入owner的名字 ")
        for item in self.search_name(name):
            guess_name = item[0]
            
            print(Panel.fit('[green]' + guess_name[0] + ' ' + guess_name[1]+ '\n' +'[blue]' + self.info(guess_name)[0][0] + '\n' + '[blue]' + self.info(guess_name)[0][1]))
            
            command = input('您是指上面这个员工吗？(y/n) ')
            while(command.lower() not in ['y','n']):
                command = input('请正确输入命令, 仅接受y和n ')

            if command.lower() == 'y':
                self.first_name = guess_name[0]
                self.last_name = guess_name[1]
                self.department = self.info(guess_name)[0][0]
                self.location = self.info(guess_name)[0][1]
                break
    
    def wave_conversation(self):
        '''
        the conversation for the waves
        '''
        wave = IntPrompt.ask("这是第几波呢？",default=1)
        return
            



if __name__ == "__main__":
    c = Create()
    c.wave_conversation()

    
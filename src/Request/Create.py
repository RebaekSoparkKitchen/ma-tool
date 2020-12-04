"""
@Description:
@Author: FlyingRedPig
@Date: 2020-11-24 11:23:07
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-26 12:00:38
@FilePath: \MA_tool\src\Request\Create.py
"""
import sys
sys.path.append("../..")
import datetime as dt
from src.Control.MA import MA
from src.Utils.Similarity import Similarity
from rich import print
from rich.panel import Panel
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

        self.request_id = 0
        self.first_name = ''
        self.last_name = ''
        self.wave = 1
        self.blast_date = None
        self.event_date = None
        self.blast_date_str = ''
        self.event_date_str = ''
        self.department = ''
        self.location = ''
        self.request_type = ''
        self.campaign_name = ''
        self.comment = ''

    def search_name(self, input_name: str) -> list:
        """
        name: the input name
        """
        new_name = []
        for name in self.name_list:
            new_name.append([name, Create.compare_name(name, input_name)])

        new_name.sort(key=lambda x: x[1], reverse=True)
        return new_name

    @staticmethod
    def compare_name(standard_name: tuple, input_name: str) -> float:
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
        return self.sqlProcess(
            f"SELECT department, location FROM Staff WHERE first_name = '{name[0]}' AND last_name = '{name[1]}'")

    def name_dialogue(self, default: str = '') -> None:
        """
        the conversation for name confirmation
        """
        name_completer = WordCompleter(list(map(lambda x: ' '.join(x), c.name_list)), ignore_case=True,
                                       match_middle=True)
        name = prompt('请输入owner的名字: ', completer=name_completer, complete_while_typing=True, key_bindings=short_cut(),
                      default=default)
        for item in self.search_name(name):
            guess_name = item[0]

            print(Panel.fit(
                '[green]' + guess_name[0] + ' ' + guess_name[1] + '\n' + '[blue]' + self.info(guess_name)[0][
                    0] + '\n' + '[blue]' + self.info(guess_name)[0][1]))

            command = Confirm.ask('您是指上面这个员工吗？', default=True)

            if command:
                self.first_name = guess_name[0]
                self.last_name = guess_name[1]
                self.department = self.info(guess_name)[0][0]
                self.location = self.info(guess_name)[0][1]
                break
        return

    def wave_dialogue(self, default: int = 1):
        """
        the conversation for the waves
        """
        wave = IntPrompt.ask('这是第几波EDM？', default=default)
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

    def blast_date_dialogue(self, default: str = '2020'):
        """
        main method
        let user input blast date
        """
        while True:
            date = prompt('请输入 blast date: ', default=default)
            while date == '':
                command = Confirm.ask('您确认此需求没有blast date吗', default=True)
                if command:
                    self.comment = Prompt.ask('您没有输入blast date，请备注')
                    return
                else:
                    date = prompt('请输入 blast date: ', default=default)
            try:
                blast_date = dt.datetime.strptime(date, '%Y%m%d').date()
                if not Create.confirm_date(blast_date, dt.date.today(), '[#ffc107]您输入的blast date日期在今天之前，您确定吗？'):
                    continue
                self.blast_date_str = date
                self.blast_date = blast_date
                break
            except ValueError:
                print('[prompt.invalid]请输入正确的日期格式，eg: 20201125')
        return

    def event_date_dialogue(self, default: str = '2020'):
        """
        main method
        let user input event date
        """
        while True:
            date = prompt('请输入 event date: ', default=default)
            # 如果blast date是空值，well，我还没想好怎么处理这个情况，先try except pass吧
            try:
                event_date = dt.datetime.strptime(date, '%Y%m%d').date()
                if not Create.confirm_date(event_date, dt.date.today(), '[#ffc107]此日期在今天之前，您确定吗'):
                    continue
                try:
                    event_date = dt.datetime.strptime(date, '%Y%m%d').date()
                    if not Create.confirm_date(event_date, self.blast_date, '[#ffc107]此日期在blast date之前，您确定吗'):
                        continue
                except TypeError:
                    pass
                self.event_date_str = date
                self.event_date = event_date
                break
            except ValueError:
                print('[prompt.invalid]请输入正确的日期格式，eg: 20201125')
        return

    def request_type_dialogue(self, default: str = 'Webinar Invitation'):
        """
        dialogue -> create new request type
        """
        type_list = ['Webinar Invitation', 'Offline Event Invitation', 'EDM', 'Newsletter']
        type_completer = WordCompleter(type_list, ignore_case=True, match_middle=True)
        while True:
            request_type = prompt('请输入 Request Type: ', default=default, completer=type_completer,
                                  complete_while_typing=True,
                                  key_bindings=short_cut())
            if request_type not in type_list:
                print('请输入正确的type，请参考')
                print(','.join(type_list))
            else:
                break
        self.request_type = request_type
        return

    def campaign_name_dialogue(self, default: str = ''):
        """
        dialogue for campaign name
        :return: None
        """
        campaign_name = prompt('请输入 Campaign name: ', default=default)
        self.campaign_name = campaign_name
        return

    def confirm_dialogue(self):
        """
        dialogue for final confirm
        :return: None
        """
        while True:
            info = str(f'[green]Wave:[/green] [blue]{self.wave}[blue] \n' +
                       f'[green]Campaign Name:[/green] [blue]{self.campaign_name}[/blue] \n' +
                       f'[green]Request Type:[/green] [blue]{self.request_type}[/blue] \n' +
                       f'[green]Owner:[/green] [blue]{self.first_name} {self.last_name}[/blue] \n' +
                       f'[green]Department:[/green] [blue]{self.department}[/blue] \n' +
                       f'[green]Location:[/green] [blue]{self.location}[/blue] \n' +
                       f'[green]Blast Date:[/green] [blue]{self.blast_date}[/blue]')
            if self.request_type in ['Webinar Invitation', 'Offline Event Invitation']:
                print(Panel.fit(
                    info + f'\n[green]Event Date:[/green] [blue]{self.event_date}[/blue]'
                ))
            else:
                print(Panel.fit(info))
            command = Confirm.ask('请最终确定一下此request的信息', default=True)
            if command:
                # 最终确定时，如果type改为非invitation， 那么event date要清掉
                if self.request_type not in ['Webinar Invitation', 'Offline Event Invitation']:
                    self.event_date_str = ''
                    self.event_date = None
                break
            else:
                self.wave_dialogue(default=self.wave)
                self.name_dialogue(default=self.first_name + ' ' + self.last_name)
                self.campaign_name_dialogue(default=self.campaign_name)
                self.request_type_dialogue(default=self.request_type)
                self.blast_date_dialogue(default=self.blast_date_str)
                if self.request_type in ['Webinar Invitation', 'Offline Event Invitation']:
                    self.event_date_dialogue(default=self.event_date_str)
        return



    def creation_dialogue(self):
        self.wave_dialogue()
        self.name_dialogue()
        self.campaign_name_dialogue()
        self.request_type_dialogue()
        self.blast_date_dialogue()
        if c.request_type in ['Webinar Invitation', 'Offline Event Invitation']:
            c.event_date_dialogue()
        self.confirm_dialogue()
        return


if __name__ == "__main__":
    # 明日任务： wave 2 的处理 request id的处理
    c = Create()
    a = c.creation_dialogue
    print(type(a))
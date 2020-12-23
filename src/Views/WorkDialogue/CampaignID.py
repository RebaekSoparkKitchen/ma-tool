from prompt_toolkit.validation import Validator
from rich.prompt import Confirm
from src.Views.Dialogue import Dialogue


class CampaignID(Dialogue):
    def __init__(self, question: str = '请输入 smc campaign id: ', default: str = ''):
        super().__init__(question, default)

    def validator(self):
        return Validator.from_callable(
            lambda x: x.isdigit or (not x),
            error_message='smc campaign id should be numbers',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        if not text:
            while not Confirm.ask("Are you sure you don't want to type in an smc_campaign_id for this request?")
                self.ask()
        return text
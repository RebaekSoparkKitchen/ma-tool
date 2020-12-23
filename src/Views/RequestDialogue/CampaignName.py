import sys

sys.path.append("../..")
from prompt_toolkit.validation import Validator
from src.Views.RequestDialogue.Dialogue import Dialogue
from src.Models.Request import Request


class CampaignName(Dialogue):
    def __init__(self, request: Request, question: str = '请输入Campaign Name: ', default: str = ''):
        super().__init__(request, question, default)

    def validator(self):
        return Validator.from_callable(
            lambda x: x,
            error_message='The campaign name can not be blank',
            move_cursor_to_end=True
        )

    def guess(self, text, question, default):
        return text

    def warning(self, text, question, default):
        return text


if __name__ == '__main__':
    r = Request()
    c = CampaignName(r)
    print(c.ask())

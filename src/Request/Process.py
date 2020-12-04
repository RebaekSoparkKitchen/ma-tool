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
from collections.abc import Callable
from src.Request.Dialogue import Dialogue
from prompt_toolkit.validation import Validator


def is_number(text):
    return text.isdigit()


if __name__ == '__main__':
    validator = Validator.from_callable(
        is_number,
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)
    wave = Dialogue('请问是第几波？', default='1', validator=validator)
    wave.ask()

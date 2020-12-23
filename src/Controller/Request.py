import sys

sys.path.append("../..")
from src.Views.RequestDialogue.Register import register
from src.Models.Request import Request


def create():
    r = Request()
    register(r).create()
    return


if __name__ == '__main__':
    create()

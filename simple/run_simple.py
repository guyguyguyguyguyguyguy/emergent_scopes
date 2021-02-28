from typing import Final
from model import Model

WIDTH: Final = 500
HEIGHT: Final = 500


def run():

    m = Model(width= WIDTH, height= HEIGHT)
    m.run()


run()

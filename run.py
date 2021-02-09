from typing import Final
from model import Model

WIDTH: Final = 50
HEIGHT: Final = 50


def run(WIDTH, HEIGHT):

    m = Model(WIDTH, HEIGHT)
    m.run()

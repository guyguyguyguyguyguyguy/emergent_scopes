from typing import Final
from model import Model

WIDTH: Final = 500
HEIGHT: Final = 500
AGENTS: Final = 30

def run():

    m = Model(width= WIDTH, height= HEIGHT, num_agents= AGENTS)
    m.run()


run()

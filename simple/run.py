from typing import Final
from model import Model
import sys

WIDTH: Final = 900
HEIGHT: Final = 600

try:
    if sys.argv[1] == 'False':
        TEST = False
        AGENTS = 50
    else:
        TEST = True
        AGENTS = 0 
except:
    TEST = True
    AGENTS = 0


# Runs slowwwwwww
def run():

    m = Model(width= WIDTH, height= HEIGHT, num_agents= AGENTS, test= TEST)
    m.run()


run()

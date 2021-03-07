from typing import Final
from model import Model
import sys

WIDTH: Final = 1000
HEIGHT: Final = 700
AGENTS: Final = 0

try:
    if sys.argv[1] == 'True':
        TEST = True
    else:
        TEST = False
except:
    TEST = True

print(Final)

def run():

    m = Model(width= WIDTH, height= HEIGHT, num_agents= AGENTS, test= TEST)
    m.run()


run()

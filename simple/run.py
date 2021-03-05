from typing import Final
from model import Model
import sys

WIDTH: Final = 500
HEIGHT: Final = 500
AGENTS: Final = 0
if sys.argv[1] == 'True':
    TEST: Final = True
else:
    TEST: Final = False
print(Final)

def run():

    m = Model(width= WIDTH, height= HEIGHT, num_agents= AGENTS, test= TEST)
    m.run()


run()

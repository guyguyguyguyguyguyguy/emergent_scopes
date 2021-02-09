from agent import Agent
from typing import Type

def agent_step(agent: Agent, other_agents: list[Type[Agent]]):
   agent.step(other_agents) 


class abstractstatic(staticmethod):
    __slots__ = ()
    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True
    __isabstractmethod__ = True

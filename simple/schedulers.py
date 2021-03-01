from __future__ import annotations
import random
import copy
from abc import abstractmethod
import agent
from typing import Callable, Iterator, List
import sys


class Scheduler:

    def __init__(self) -> None:
        pass


    def __new__(cls) -> None:
        pass


    @staticmethod
    @abstractmethod
    def scheduling(agent_list: List[agent.Agent], func: Callable[[agent.Agent, List[agent.Agent]], None]) -> None:
        pass


class Asynchronous(Scheduler):

    def __init__(self) -> None:
        super().__init__()


    #possibly some generator but probably no need with random sample
    #@staticmethod
    #def sample_agents(agent_list: List[Type[agent.Agent]]) -> Iterator[agent.Agent]:
    #   pass     


    @staticmethod
    def scheduling(agent_list: List[agent.Agent], func: Callable[[agent.Agent, List[agent.Agent]], None]) -> None:
        order = random.sample(agent_list, len(agent_list))
        for a in order:
            other_agents = [x for x in agent_list if x is not a]
            func(a, other_agents)


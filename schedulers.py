from random import random
import copy
from helper import abstractstatic
from agent import Agent
from typing import Callable, Iterator, Type


class Scheduler:

    def __init__(self) -> None:
        pass


    def __new__(cls) -> None:
        pass


    @abstractstatic
    def scheduling(agent_list: list[Type[Agent]], func: Callable[[Agent, list[Type[Agent]]], None]) -> None:
        pass


class Asynchronous(Scheduler):

    def __init__(self) -> None:
        super().__init__()

    
    #possibly some generator but probably no need with random sample
    #@staticmethod
    #def sample_agents(agent_list: list[Type[Agent]]) -> Iterator[Agent]:
    #   pass     

    
    @staticmethod
    def scheduling(agent_list: list[Type[Agent]], func: Callable[[Agent, list[Type[Agent]]], None]) -> None:
        order = random.sample(agent_list, len(agent_list))
        for a in order:
            other_agents = [x for x in agent_list if x is not a]
            func(a, other_agents) 


class Parallel(Scheduler):

    """ 
        Parallel scheduler.

        All possible errors need to be accounted for eg: two agents end up on the same cell, agent is removed but also required by another agent
    """

    def __init__(self) -> None:
        super().__init__()

    
    # Make a deep copy of agent list after the previous tick and each one sees this instead of the updated one
    # Pretty sure deepcopy is the correct function 
    # Need to add cases, to ensure that no errors occur
    @staticmethod
    def scheduling(agent_list: list[Type[Agent]], func: Callable[[Agent, list[Type[Agent]]], None]) -> None:
        current_state = copy.deepcopy(agent_list)
        order = random.sample(agent_list, len(agent_list))
        for a in order: 
            other_agents = [x for x in current_state if x is not a]
            func(a, other_agents)


class Concurrent(Scheduler):

    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    def scheduling(agent_list: list[Type[Agent]], func: Callable[[Agent, list[Type[Agent]]], None]) -> None:
        pass

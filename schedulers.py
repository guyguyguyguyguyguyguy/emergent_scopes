from random import random
import copy
from helper import abstractstatic
from agent import Agent
from typing import Callable, Iterator, Type
import sys


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
    
        try:
            # Think this changes the model agent list in place
            # This isn't exactly what we want but its on the right lines, maybe?
            equal_agents = [[x,y] for x in current_state for y in current_state if x==y]
            for pair in equal_agents:
                blocked = random.choice(pair)
                # Replacing updated agent in current_state with the state of the agent in the previous tick as it has been blocked from is behaviour by another agent that is occupying the same phase space (with assumption that no two agents can occupy same phase space)
                # This is context specific, == has to be defined for agents in a certain manner
                current_state[current_state.index(blocked)] = agent_list[agent_list.index(blocked)]
            agent_list[:] = current_state
        except:
            print("Could not combine agents in current tick")
            sys.exit(1)
        else:
            pass


class Concurrent(Scheduler):

    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    def scheduling(agent_list: list[Type[Agent]], func: Callable[[Agent, list[Type[Agent]]], None]) -> None:
        pass

from random import random
import copy
from helper import abstractstatic
from agent import Agent
from typing import Callable, Iterator, List
import sys


class Scheduler:

    def __init__(self) -> None:
        pass


    def __new__(cls) -> None:
        pass


    @abstractstatic
    def scheduling(agent_list: List[Agent], func: Callable[[Agent, List[Agent]], None]) -> None:
        pass


class Asynchronous(Scheduler):

    def __init__(self) -> None:
        super().__init__()

    
    #possibly some generator but probably no need with random sample
    #@staticmethod
    #def sample_agents(agent_list: List[Type[Agent]]) -> Iterator[Agent]:
    #   pass     

    
    @staticmethod
    def scheduling(agent_list: List[Agent], func: Callable[[Agent, List[Agent]], None]) -> None:
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

    
    # Make a deep copy of agent List after the previous tick and each one sees this instead of the updated one
    # Pretty sure deepcopy is the correct function 
    # Need to add cases, to ensure that no errors occur
    def scheduling(self, agent_list: List[Agent], func: Callable[[Agent, List[Agent]], None]) -> None:
        current_state = copy.deepcopy(agent_list)
        order = random.sample(agent_list, len(agent_list))
        for a in order: 
            other_agents = [x for x in current_state if x is not a]
            func(a, other_agents)
    
        agent_list[:] = self.__clash_solution(copy.deepcopy(agent_list), current_state)
        
    
    @staticmethod
    def __clash_solution(previous_state: List[Agent], next_state: List[Agent]) -> List[Agent]:
        """
            Want to check each of the possible behaviours:
                -> See if there are any conditionals
                -> If so, test whether these conditionals are broken by another agents move
                -> Solve conflicts:
                    - This will incur randomness as conflicts solved randomly
                -> Return 'conflict-free list of agents'

            $Not possible$

            Maybe:
                -> User writes conditions that should not be broken
                    - Would be nice to derive these conditons from the behaviours
                -> Then check for conflicts of these conditions and solve
        """

        try:
            # Think this changes the model agent List in place
            # This isn't exactly what we want but its on the right lines, maybe?
            equal_agents = [[x,y] for x in next_state for y in next_state if x==y]
            for pair in equal_agents:
                blocked = random.choice(pair)
                # Replacing updated agent in current_state with the state of the agent in the previous tick as it has been blocked from is behaviour by another agent that is occupying the same phase space (with assumption that no two agents can occupy same phase space)
                # This is context specific, == has to be defined for agents in a certain manner
                next_state[next_state.index(blocked)] = previous_state[previous_state.index(blocked)]
                
                return next_state
        except:
            print("Could not combine agents in current tick")
            sys.exit(1)
        else:
            return next_state


class Concurrent(Scheduler):

    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    def scheduling(agent_list: List[Agent], func: Callable[[Agent, List[Agent]], None]) -> None:
        pass

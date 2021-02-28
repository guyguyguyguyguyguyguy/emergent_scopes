from abc import abstractclassmethod, abstractmethod, ABC
import random
from typing import List, Tuple
from operator import add
#import agent 
#TODO: type hinting with agent: agent.Agent but this is circular importing so need to find solution

class Behaviour(ABC):

    @abstractmethod
    def step(selft, agent) -> None:
        pass


class RandMov(Behaviour):

    """
        RandMove provides agents with behaviour representing random movement.
        Takes an agents current position and returns a new position depending on agents step size
    """ 


    def __init__(self) -> None:
        self.step_size = random.randint(1, 10) 


    def step(self, agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """
        
        move_vector = random.sample([-1, 0, 1], 2)
        agent.pos = list(map(add, move_vector, agent.pos)) 
    

class Adhesion(Behaviour):
    """
        Agents with this behaviour stick together
        Possibilities:
            -> can only attach n number of others
            -> Have some sort of intrinsic directionality (top, bottom, sides)
                - Can only connect to side (or something else)
    """

    def __init__(self) -> None:
        self.strength = random.randint(1, 10)

    
    def step(self, agent) -> None:
        """
            Checks if near agents have this behviour:
                -> If so, move closer to this agent (based on strength)
                -> Cohesive agents become a single agent
                -> Garbage keeping over individual agents that are now cohesive
        """
        pass
        

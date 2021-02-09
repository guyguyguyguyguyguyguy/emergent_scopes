from abc import abstractclassmethod, abstractmethod
import random
from agent import Agent 


@abstractclassmethod
class Behaviour(object):
    
    @abstractmethod
    def step(self, agent: Agent):
        pass


class RandMov(Behaviour):

    """
        RandMove provides agents with behaviour representing random movement.
        Takes an agents current position and returns a new position depending on agents step size.
    """ 

    def __init__(self) -> None:
        self.step_size = random.randint(1, 10) 

    
    def step(self, agent : Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """
        
        move_vector = random.sample([-1, 0, 1], 2)
        agent.pos += [x*self.step_size for x in move_vector]

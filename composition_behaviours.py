from abc import abstractclassmethod, abstractmethod
import random
from typing import List, Tuple
from agent import Agent 


@abstractclassmethod
class Behaviour:
   
    @property
    @abstractmethod
    def constraints(self):
        pass


    @abstractmethod
    def constraint(anget: List[Agent]) -> List[Tuple[Agent, List[Agent]]]:
        pass


    @abstractmethod 
    def resolution(agents: List[Tuple[Agent, List[Agent]]]) -> None:
        pass


    @abstractmethod
    def step(self, agent: Agent) -> None:
        pass


class RandMov(Behaviour):

    """
        RandMove provides agents with behaviour representing random movement.
        Takes an agents current position and returns a new position depending on agents step size
    """ 


    def __init__(self) -> None:
        self.step_size = random.randint(1, 10) 
  

    @property
    def constraints(self):
        return self._constrains

    @constraints.setter
    def constraints(self): 
        self._constrains = {"no overlap": self.overlap_constraint} 
    

    def overlap_constraint(self, agents: List[Agent]) -> List[Tuple[Agent, List[Agent]]]:
        """
            Return either bool of whether conflicts resolved by resolution 
            orrr
            Return list of list of conflicting agent with others, although this leads to duplicates
        """
        conflicts = [] 
        for a in agents:
            a_conflict = (a, )
            other = [o for o in agents if o is not a and o.pos != a.pos]
            conflicting_agents = (*a_conflict, other)
            conflicts.append(conflicting_agents)
            self.resolution(conflicting_agents) 
        return conflicts


    def resolution(self, agents: Tuple[Agent, List[Agent]]) -> None:
        """
            Resloves agents that share the same space by small collision between them
        """
        a, other = agents
        self.collision([a, *other])


    @staticmethod
    def collision(elements: List[Agent]) -> None:
        #TODO: Sort this method, however, only needed for parallel shit 
        pass

        
    def step(self, agent : Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """
        
        move_vector = random.sample([-1, 0, 1], 2)
        agent.pos += [x*self.step_size for x in move_vector]
    

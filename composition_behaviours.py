from abc import abstractclassmethod, abstractmethod, abstract_attribute
import random
from helper import abstractstatic
from agent import Agent 


@abstractclassmethod
class Behaviour:
   
    @abstract_attribute
    def constraints(self) -> dict[str, Callable[List[Agents], bool]]:
        pass

    
    @abstractstatic
    def constraint(agents: List[Agent]) -> bool:
        pass


    @abstractstatic
    def resolution(agents: List[Agent, List[Agent]]) -> None:
        pass


    @abstractmethod
    def step(self, agent: Agent) -> None:
        pass


class RandMov(Behaviour):

    """
        RandMove provides agents with behaviour representing random movement.
        Takes an agents current position and returns a new position depending on agents step size
    """ 

    constraints = {"no overlap": self.constraint} 

    def __init__(self) -> None:
        self.step_size = random.randint(1, 10) 


    @staticmethod
    def constraint(agents: List[Agent]) -> bool:
        """
            Return either bool of whether conflicts resolved by resolution 
            orrr
            Return list of list of conflicting agent with others, although this leads to duplicates
        """
        conflicts = []
        for a in agents:
            while other := len([o for o in agents if o is not a and o.x != a.x and o.y != a.y]) > 0:
               # resolution([a].append(others)) 
                conflicts.append([a].append(others))
        return conflicts
    

    @staticmethod
    def resolution(List[Agent, List[Agent]]) -> None:
       pass 
        
        

    @staticmethod
    def step(self, agent : Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """
        
        move_vector = random.sample([-1, 0, 1], 2)
        agent.pos += [x*self.step_size for x in move_vector]
    

import random
from typing import Type
from model import *
from composition_behaviours import Behaviour 


class Agent():

    """Docstring for Agent. """

    def __init__(self, *behaviours: list[Type[Behaviour]], model: Model) -> None:
        """.
            Initalise Agent class with n number of composite behaviours.

            Parameters: 
                *behaviours (list) : Defines all behaviours recieved by Agent.
        """
        
        self.behaviours = behaviours
        self.pos = [random.choice(range(model.width)), random.choice(range(model.height))]


    def step(self, other_agents: list[Type[Agent]]) -> None:
        """
            Allows each of Agents behaviours to act. Is dependent on the order of *behviours so need to be careful
        """
        # Envisage some of these taking a list of other agents, hence why this method takes a list of agents
        # Depending on scheduling class used in mode, this will either be a copy or the current
        for x in self.behaviours:
            x.step(self)

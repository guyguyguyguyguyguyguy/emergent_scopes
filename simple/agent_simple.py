from __future__ import annotations
import random
from typing import List 
import model 
from composition_behaviours import Behaviour 
from collections.abc import Sequence, Iterable


class Agent:

    """Docstring for Agent. """

    def __init__(self, behaviours: Iterable[Behaviour], model: model.Model) -> None:
        """.
            Initalise Agent class with n number of composite behaviours.

            Parameters: 
                *behaviours (list) : Defines all behaviours recieved by Agent.
        """
        
        self.behaviours = behaviours
        self.pos = [random.choice(range(model.width)), random.choice(range(model.height))]


    def __eq__(self, o: Agent) -> bool:
        if self.pos == o.pos:
            return True
        else:
            return False

    def step(self, other_agents: List[Agent]) -> None:
        """
            Allows each of Agents behaviours to act. Is dependent on the order of *behviours so need to be careful
        """
        # Envisage some of these taking a list of other agents, hence why this method takes a list of agents
        # Depending on scheduling class used in mode, this will either be a copy or the current
        for x in self.behaviours:
            x.step(self)


class CohesiveAgents:
    pass

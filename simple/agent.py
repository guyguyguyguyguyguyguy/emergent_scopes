from __future__ import annotations
import random
from typing import List
import numpy as np
import model
from composition_behaviours import Behaviour
from collections.abc import Sequence, Iterable
from dataclasses import dataclass

# Not using this but good for learning
@dataclass
class Pos:
    x: float
    y: float

    def __repr__(self):
        return repr([self.x, self.y])


    def __getitem__(self, k: int) -> float:
             return [self.x, self.y][k]


    def __setitem__(self, k: int, v:float) -> None:
        self[k] = v


    def __eq__(self, o: Pos) -> bool:
        if self.x == o.x and self.y == o.y:
            return True
        else:
            return False


    def __iter__(self) -> Iterable[float]:
        return iter([self.x, self.y])


    # Don't know what type to give x
    def __add__(self, x) -> Pos:
        return Pos(self.x + x[0], self.y + x[1])


class Agent:

    """
        Carrier class for composition behaviours:
    """

    def __init__(self, behaviours: Iterable[Behaviour], model: model.Model, pos: np.ndarray = None, radius: int = None) -> None:
        """.
            Initalise Agent class with n number of composite behaviours.

            Parameters:
                behaviours (list) : Defines all behaviours recieved by Agent.
                radius (int) : radius and weight of the agent. Used in collisions for RandMov behaviour and as radius in visalisation
                v (list[float]) : velocity of agent in x and y axes, initalised as 0
                pos (list[float]) : inital position of the agent
        """

        self.radius = random.randint(15, 25) if not radius else radius
        self.v = np.array([0, 0])
        self.behaviours = behaviours
        self.model = model
        self.pos = np.array([ random.choice(range(model.width)), random.choice(range(model.height)) ]) if pos is None else pos


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

from __future__ import annotations
from abc import abstractclassmethod, abstractmethod, ABC
import random
from typing import List, Tuple
from operator import add
import helper
import agent 
#TODO: type hinting with agent: agent.Agent but this is circular importing so need to find solution


# Element-wise list addition 'MACRO'
elem_add = lambda x, y: list(map(add, x, y))


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


    def in_bounds(self, agent: agent.Agent) -> None:
        """
            Keep agent in boundaries of canvas
        """
        if agent.pos[0] - agent.radius < 0:
            agent.pos[0] = agent.radius
            agent.v[0] = -agent.v[0]
        if agent.pos[0] + agent.radius > agent.model.width:
            agent.pos[0] = agent.model.width-agent.radius
            agent.v[0] = -agent.v[0]
        if agent.pos[1] - agent.radius < 0:
            agent.pos[1] = agent.radius
            agent.v[1] = -agent.v[1]
        if agent.pos[1] + agent.radius > agent.model.height:
            agent.pos[1] = agent.model.height-agent.radius
            agent.v[1] = -agent.v[1]


    #Todo: Not sure this works properly?
    def step(self, agent: agent.Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """

        move_vector = random.sample([-0.05, 0, 0.05], 2)
        agent.v =elem_add(move_vector, agent.v)
        agent.pos = elem_add(agent.v, agent.pos)
        if shared_pos := [x for x in agent.model.agents if x != agent and helper.distance(agent, x) < agent.radius]:
            helper.collide(agent, shared_pos, len(shared_pos)+1)
            agent.pos = elem_add(agent.v, agent.pos)

        self.in_bounds(agent)


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


    def step(self, agent: agent.Agent) -> None:
        """
            Checks if near agents have this behviour:
                -> If so, move closer to this agent (based on strength)
                -> Cohesive agents become a single agent
                -> Garbage keeping over individual agents that are now cohesive
        """
        pass


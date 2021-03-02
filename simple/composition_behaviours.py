from __future__ import annotations
from abc import abstractclassmethod, abstractmethod, ABC
import random
import numpy as np
from itertools import combinations
from typing import List, Tuple
from operator import add
import helper
import agent 


def in_bounds(agent: agent.Agent) -> None:
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


    @staticmethod
    def collide(agent: agent.Agent, other_agents: List[agent.Agent]) -> None:
        """Detect and handle any collisions between the Particles.

        When two Particles collide, they do so elastically: their velocities
        change such that both energy and momentum are conserved.

            agent (Agent) : agent that function was called by 
            other_agents (List) : list of other agents involved in collision

        """

        def change_velocities(p1, p2) -> None:
            """
            Particles p1 and p2 have collided elastically: update their
            velocities.

            """

            m1, m2 = np.array(p1.radius**2), np.array(p2.radius**2)
            M = m1 + m2
            r1, r2 = np.array(p1.pos), np.array(p2.pos)
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = np.array(p1.v), np.array(p2.v)
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.v = u1
            p2.v = u2

        # We're going to need a sequence of all of the pairs of particles when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.particles list of Particles on the fly.
        pairs = combinations([agent, *other_agents], 2)
        for i,j in pairs:
            change_velocities(i, j) 


    #Todo: Not sure this works properly?
    def step(self, agent: agent.Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """

        move_vector = random.sample([-0.05, 0, 0.05], 2)
        agent.v =helper.elem_add(move_vector, agent.v)
        agent.pos = helper.elem_add(agent.v, agent.pos)
        if shared_pos := [x for x in agent.model.agents if x is not agent and helper.distance(agent, x) < agent.radius]:
            self.collide(agent, shared_pos)
            agent.pos = helper.elem_add(agent.v, agent.pos)

        in_bounds(agent)


class Adhesion(Behaviour):
    """
        Agents with this behaviour stick together
        Possibilities:
            -> can only attach n number of others
            -> Have some sort of intrinsic directionality (top, bottom, sides)
                - Can only connect to side (or something else)
    """

    def __init__(self) -> None:
        self.strength = 25


    @staticmethod
    def attract(agent: agent.Agent, other_agents: List[agent.Agent]) -> None:
        """
            Other agents in a close radius to the agent that also have the adhesive behaviour are drawn together

            agent (Agent) : agent that function was called by 
            other_agents (List) : list of other agents involved in collision
        """

        # Not totally working need them to not go inside one another, something to do with the if statment
        def change_velocities(p1, p2):
            distance_vector = np.array(p1.pos) - np.array(p2.pos)
            move_vector = 0.1 * distance_vector
            p1.pos = helper.elem_add(p1.pos, -move_vector)
            p2.pos = helper.elem_add(p2.pos, move_vector)
            if (dist := helper.distance(p1, p2)) <= (p1.radius + p2.radius):
                x_ratio = distance_vector[0]/dist
                p1_dist = dist - p2.radius
                p2_dist = dist - p1.radius
                
                p1_move_vec = [p1_dist * x_ratio, p1_dist * (1-x_ratio)]
                p2_move_vec = [p2_dist * x_ratio, p2_dist * (1-x_ratio)]

                p1.pos = helper.elem_add(p1.pos, p1_move_vec)
                p2.pos = helper.elem_add(p2.pos, p2_move_vec)

        pairs = combinations([agent, *other_agents], 2)
        for i, j in pairs:
            change_velocities(i, j)


    def step(self, agent: agent.Agent) -> None:
        """
            Checks if near agents have this behviour:
                -> If so, move closer to this agent (based on strength)
                -> Don't get stuck inside other agent
        """
        if close_others := [x for x in agent.model.agents if x is not agent and helper.distance(agent, x) < self.strength and self in x.behaviours]:
            self.attract(agent, close_others) 

        in_bounds(agent)




from __future__ import annotations
import numpy as np
from itertools import combinations
from typing import Type, List
import agent

#def agent_step(agent: Agent, other_agents: List[Agent]):
    #   agent.step(other_agents) 


def distance(agent1: agent.Agent, agent2: agent.Agent) -> float:
    return np.linalg.norm(np.array(agent1.pos) - np.array(agent2.pos))
    

def collide(agent: agent.Agent, other_agents: List[agent.Agent], number_agents: int) -> None:
    """Detect and handle any collisions between the Particles.

    When two Particles collide, they do so elastically: their velocities
    change such that both energy and momentum are conserved.

        agent (Agent) : agent that function was called by 
        number_agents (int) : number of agents involved in collision
        other_agents (List) : list of other agents involved in collision

    """

    def change_velocities(p1, p2):
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

from __future__ import annotations
import numpy as np
from itertools import combinations
from typing import Type, List
from operator import add
import agent

#def agent_step(agent: Agent, other_agents: List[Agent]):
    #   agent.step(other_agents) 


# Element-wise list addition 'MACRO'
elem_add = lambda x, y: list(map(add, x, y))


# Find the angle that one agent lies on the other agent
def angle_on_cirumfrance(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:

    ac = np.arctan2(c[1] - a[1], c[0] - a[0])
    ab = np.arctan2(b[1] - a[1], b[0] - a[0])
    angle = ac - ab

    angle = angle - 2*np.pi if angle > np.pi else angle + 2*np.pi

    return angle 


def distance(agent1: agent.Agent, agent2: agent.Agent) -> float:
    dist = np.linalg.norm(np.array(agent1.pos) - np.array(agent2.pos))
    return dist








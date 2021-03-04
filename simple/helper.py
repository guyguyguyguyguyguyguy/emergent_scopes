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
    ab = b - a
    ac = c - a

    cosine_angle = np.dot(ab, ac) / (np.linalg.norm(ab) * np.linalg.norm(ac))
    angle = np.arccos(cosine_angle)

    return angle 


def distance(agent1: agent.Agent, agent2: agent.Agent) -> float:
    dist = np.linalg.norm(np.array(agent1.pos) - np.array(agent2.pos))
    return dist








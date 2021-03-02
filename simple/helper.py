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


def distance(agent1: agent.Agent, agent2: agent.Agent) -> float:
    return np.linalg.norm(np.array(agent1.pos) - np.array(agent2.pos))
    








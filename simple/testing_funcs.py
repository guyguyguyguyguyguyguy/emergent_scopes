from __future__ import annotations
import random
import numpy as np
import model
import agent
from composition_behaviours import Adhesion, RandMov, Linking
from typing import List, Union, Tuple
import pygame


def move_adhesion_agent_on_mouse_down(event: pygame.event, model: model.Model, dragging: bool, new_agent: Union[agent.Agent, None]) -> Tuple[bool, Union[agent.Agent, None]]:
   
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            dragging = True  
            # new_agent = agent.Agent([Adhesion(), RandMov()], model, pos = np.array(event.pos), radius = random.randint(10, 25))
            new_agent = agent.Agent([Linking(), RandMov()], model, pos = np.array(list(event.pos)), radius= 40)
            model.agents.append(new_agent)
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            dragging = False
    elif event.type == pygame.MOUSEMOTION:
        if dragging and new_agent:
            new_agent.pos = np.array(list(event.pos))

    return dragging, new_agent

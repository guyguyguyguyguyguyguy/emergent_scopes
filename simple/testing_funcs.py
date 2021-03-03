from __future__ import annotations
import model
import agent
from composition_behaviours import Adhesion, RandMov
from typing import List, Union, Tuple
import pygame


def move_adhesion_agent_on_mouse_down(event: pygame.event, model: model.Model, dragging: bool, new_agent: Union[agent.Agent, None]) -> Tuple[bool, Union[agent.Agent, None]]:
   
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            dragging = True  
            new_agent = agent.Agent([Adhesion(), RandMov()], model, pos = list(event.pos))
            model.agents.append(new_agent)
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            dragging = False
    elif event.type == pygame.MOUSEMOTION:
        if dragging and new_agent:
            new_agent.pos = list(event.pos)

    return dragging, new_agent

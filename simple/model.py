from __future__ import annotations
import sys
import numpy as np
import pygame
import random
import agent
import composition_behaviours 
import testing_funcs
from typing import TypeVar, Type, List
import schedulers


def agent_step(agent: agent.Agent, other_agents: List[agent.Agent]):
       agent.step(other_agents)


class Model:

    """
        Model for simulating emergence at multiple scales
    """

    def __init__(self, width: int = 50, height: int = 50, num_agents: int = 20, scheduler: Type[schedulers.Scheduler] = schedulers.Asynchronous, test: bool = False) -> None:
        """
            Initalise model

            Parameters:
                num_agents (int) : number of agents initalised in mode
                width (int) : width of pygame window
                height (int) : height of pygame window
                scheduler (Scheduler) : method by which agents are scheduled to perform their step method at every tick
        """
        self.width = width
        self.height = height
        self.scheduler = scheduler
        # self.behaviours = [composition_behaviours.RandMov, composition_behaviours.Adhesion]
        # self.behaviours = [composition_behaviours.Adhesion]
        self.behaviours = [composition_behaviours.RandMov]
        self.num_agents = num_agents
        self.agents = [agent.Agent(self.assign_behaviours(), model=self) for x in range(num_agents)]
        self.test = test
    

    # Way to get unique instantiation of composition behaviours in each agent
    # Must be a better way to do this
    def assign_behaviours(self) -> List[composition_behaviours.Behaviour]:
        give_behaviours = random.sample(self.behaviours, k=random.randint(1, len(self.behaviours)))
        instant_behaviours = []
        for x in give_behaviours:
            instant_behaviours.append(x())

        return instant_behaviours


    def run(self) -> None:
        done = False
        dragging = False
        ticking = False
        new_agent = None
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        if self.test:
                            self.tick()
                    elif event.key == pygame.K_r:
                        self.agents = [agent.Agent(self.assign_behaviours(), model=self) for x in range(self.num_agents)]
                    elif event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        done = True
                
                dragging, new_agent = testing_funcs.move_adhesion_agent_on_mouse_down(event, self, dragging, new_agent)
               
            if self.test:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_SPACE]:
                    self.tick()

            self.screen.fill((0, 0, 0))
            for a in self.agents:
                pygame.draw.circle(self.screen, (255, 255, 255), a.pos, a.radius)
                
            if not self.test:
                self.tick()
            
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


    #sort parralell and asynchornos scheduling
    def tick(self) -> None:
        self.scheduler.scheduling(self.agents, agent_step)


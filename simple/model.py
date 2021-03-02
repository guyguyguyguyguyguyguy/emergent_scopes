from __future__ import annotations
import numpy as np
import pygame
import random
import agent
import composition_behaviours 
#from helper import agent_step
from typing import TypeVar, Type, List
import schedulers


def agent_step(agent: agent.Agent, other_agents: List[agent.Agent]):
       agent.step(other_agents)


class Model:

    """
        Model for simulating emergence at multiple scales
    """

    def __init__(self, width: int = 50, height: int = 50, num_agents: int = 20, scheduler: Type[schedulers.Scheduler] = schedulers.Asynchronous) -> None:
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
        # self.behaviours = [composition_behaviours.RandMov(), composition_behaviours.Adhesion()]
        self.behaviours = [composition_behaviours.Adhesion()]
        self.num_agents = num_agents
        self.agents = [agent.Agent(random.sample(self.behaviours, k= random.randint(1, len(self.behaviours))), model=self) for x in range(num_agents)]
        

    def run(self) -> None:
        done = False
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        done = True
                    if event.key == pygame.K_r:
                        self.agents = [agent.Agent(self.behaviours, model=self) for x in range(self.num_agents)]
            self.screen.fill((0, 0, 0))
            for a in self.agents:
                pygame.draw.circle(self.screen, (255, 255, 255), a.pos, a.radius)

            self.tick()
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


    #sort parralell and asynchornos scheduling
    def tick(self) -> None:
        self.scheduler.scheduling(self.agents, agent_step)


from __future__ import annotations
import pygame
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

    def __init__(self, width: int = 50, height: int = 50, num_Agents: int = 20, scheduler: Type[schedulers.Scheduler] = schedulers.Asynchronous) -> None:
        """
            Initalise model

            Parameters:
                num_Agents (int) : number of agents initalised in mode
        """
        self.width = width
        self.height = height
        self.scheduler = scheduler
        behaviours = [composition_behaviours.RandMov()] 
        self.agents = [agent.Agent(behaviours, model=self) for x in range(num_Agents)]

        #This is for pygame
    
    def run(self) -> None:
        done = False
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.screen.fill((0, 0, 0))
            for a in self.agents:
                pygame.draw.circle(self.screen, (255, 255, 255), a.pos, 10)
            
            self.tick()
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


    #sort parralell and asynchornos scheduling
    def tick(self) -> None:
        self.scheduler.scheduling(self.agents, agent_step) 
    

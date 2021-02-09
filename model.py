from schedulers import Scheduler
import pygame
from composition_behaviours import *
from agent import *
from helper import agent_step


class Model(object):

    """
        Model for simulating emergence at multiple scales
    """

    def __init__(self, width: int = 50, height: int = 50, num_Agents: int = 20, scheduler: Scheduler = None) -> None:
        """
            Initalise model

            Parameters:
                num_Agents (int) : number of agents initalised in mode
        """
        self.width = width
        self.height = height
        self.scheduler = scheduler
        behaviours = [RandMov()] 
        self.agents = [Agent(behaviours, model=self) for x in range(num_Agents)]

        #This is for pygame
        pygame.init()
        self.screen = pygame.display.set_mode([width, height])
    
    def run(self) -> None:
        done = False
        clock = pygame.time.Clock()
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            self.tick()
            self.screen.fill((0, 0, 0))
            for a in self.agents:
                pygame.draw.circle(self.screen, (255, 255, 255), a.pos, 10)
            
            clock.tick(60)
            pygame.display.flip()

        pygame.quit()


    #sort parralell and asynchornos scheduling
    def tick(self) -> None:
        self.scheduler.scheduling(self.agents, agent_step) 
    

import pygame
from composition_behaviours import *
from agent import *

class Model(object):

    """
        Model for simulating emergence at multiple scales
    """

    def __init__(self, width: int = 50, height: int = 50, num_Agents: int = 20) -> None:
        """
            Initalise model

            Parameters:
                num_Agents (int) : number of agents initalised in mode
        """
        self.width = width
        self.height = height
        behaviours = [RandMov()] 
        self.agents = [Agent(behaviours, model=self) for x in range(num_Agents)]

    def run(self) -> None:
        for a in self.agents:
            a.step()

        

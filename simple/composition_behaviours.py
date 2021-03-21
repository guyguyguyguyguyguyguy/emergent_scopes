from __future__ import annotations
from abc import abstractclassmethod, abstractmethod, ABC
import random
import numpy as np
from itertools import combinations
from typing import List, Tuple
from operator import add
import helper
import agent


def in_bounds(agent: agent.Agent) -> None:
    """
        Keep agent in boundaries of canvas
    """
    if agent.pos[0] - agent.radius < 0:
        agent.pos[0] = agent.radius
        agent.v[0] = -agent.v[0]
    if agent.pos[0] + agent.radius > agent.model.width:
        agent.pos[0] = agent.model.width-agent.radius
        agent.v[0] = -agent.v[0]
    if agent.pos[1] - agent.radius < 0:
        agent.pos[1] = agent.radius
        agent.v[1] = -agent.v[1]
    if agent.pos[1] + agent.radius > agent.model.height:
        agent.pos[1] = agent.model.height-agent.radius
        agent.v[1] = -agent.v[1]


class Behaviour(ABC):

    @abstractmethod
    def step(self, agent) -> None:
        pass


class RandMov(Behaviour):

    """
        RandMove provides agents with behaviour representing random movement.
        Takes an agents current position and returns a new position depending on agents step size
    """


    def __init__(self) -> None:
        self.step_size = random.randint(1, 10)


    @staticmethod
    def collide(agent: agent.Agent, other_agents: List[agent.Agent]) -> None:
        """Detect and handle any collisions between the Particles.

        When two Particles collide, they do so elastically: their velocities
        change such that both energy and momentum are conserved.

            agent (Agent) : agent that function was called by 
            other_agents (List) : list of other agents involved in collision

        """

        def change_velocities(p1, p2) -> None:
            """
            Particles p1 and p2 have collided elastically: update their
            velocities.

            """

            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = np.array(p1.pos), np.array(p2.pos)
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = np.array(p1.v), np.array(p2.v)
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.v = u1
            p2.v = u2

        
        # For some reason it doesnt really work and its so sad, but other one seems to work
        def change_velocities_2(p1, p2) -> None:
            dist = helper.distance(p1, p2)
            distance_vec = np.array(p1.pos) - np.array(p2.pos)
            norm = distance_vec/(dist)
            
            k = np.array(p1.v) - np.array(p2.v)
            p = 2 * (norm * k) / (p1.radius + p2.radius)
            p1.v = np.array(p1.v) + p * p2.radius * norm * 0.1
            p2.v = np.array(p2.v) - p * p1.radius * norm * 0.1


        # We're going to need a sequence of all of the pairs of particles when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.particles list of Particles on the fly.
        pairs = combinations([agent, *other_agents], 2)
        for i,j in pairs:
            change_velocities(i, j) 
            # change_velocities_2(i, j)


    #Todo: Not sure this works properly?
    def step(self, agent: agent.Agent) -> None:
        """
            Move agent that this instance belong to by a random vector, scaled by step size
        """

        move_vector = np.array(random.sample([-0.5, 0, 0.5], 2))
        # Idea to scale velocity by agent 'weight' (radius)
        scaled_vel = move_vector * (1/agent.radius)
        agent.v = scaled_vel + agent.v
        agent.pos = agent.v + agent.pos
        if shared_pos := [x for x in agent.model.agents if x is not agent and helper.distance(agent, x) < agent.radius]:
            self.collide(agent, shared_pos)
            agent.pos = agent.v + agent.pos

        in_bounds(agent)


class Adhesion(Behaviour):
    """
        Agents with this behaviour stick together
        Possibilities:
            -> can only attach n number of others
            -> Have some sort of intrinsic directionality (top, bottom, sides)
                - Can only connect to side (or something else)
    """

    def __init__(self) -> None:
        self.strength = random.randint(1, 4)


    @staticmethod
    def attract(agent: agent.Agent, other_agents: List[agent.Agent]) -> None:
        """
            Other agents in a close radius to the agent that also have the adhesive behaviour are drawn together

            agent (Agent) : agent that function was called by 
            other_agents (List) : list of other agents involved in collision
        """

        # Works, but not when one agent is placed (found) inside another
        # Also does not work too well when there are more than 3 balls next to each other
        def change_velocities(p1, p2):
            distance_vector = np.array(p1.pos) - np.array(p2.pos)
            move_vector = 0.1 * distance_vector
            p1.pos = p1.pos - move_vector
            p2.pos = p2.pos + move_vector
            if (dist := helper.distance(p1, p2)) <= (p1.radius + p2.radius):
                overlap = 0.5 * (dist - p1.radius - p2.radius)
                p1.pos[0] -= overlap * (p1.pos[0] - p2.pos[0]) / dist
                p1.pos[1] -= overlap * (p1.pos[1] - p2.pos[1]) /dist
                p2.pos[0] += overlap * (p1.pos[0] - p2.pos[0]) / dist
                p2.pos[1] += overlap * (p1.pos[1] - p2.pos[1]) /dist


        pairs = combinations([agent, *other_agents], 2)
        for i, j in pairs:
            change_velocities(i, j)


    def attracting_neighbours(self, agent: agent.Agent) -> List[agent.Agent]:
        attractors = []
        if len(agents := agent.model.agents) > 1:
            for a in [other for other in agents if agent is not other]:
                distance = self.strength + agent.radius + a.radius 
                if helper.distance(agent, a) <= distance:
                    if any([isinstance(b, type(self)) for b in a.behaviours]):
                        attractors.append(a)
        
        return attractors 


    # Function to ensure only n number of agents are attracted to each agent
    #   -> Possibly want to add some sort of polarity to the agent such that can only be attracted on certain side
    #   -> Thinking of lipposaccharides forming a single-layer membrane
    # Repuled by other attracted agent by distance of agent radius (should attract it to other side)
    # Todo: NEEDS WERK!
    def attraction_constraints(self, agent: agent.Agent) -> None:
        bound_others = [x for x in agent.model.agents if x is not agent and helper.distance(agent, x) <= (x.radius + agent.radius + self.strength) and any([isinstance(b, type(self)) for b in x.behaviours])] 
        # Kinda works, for now
        while len(bound_others) > 2:
            repelled_agent = bound_others.pop()
            move_vec = -repelled_agent.v
            repelled_agent.pos += move_vec

        # If distance is less than diameter of agent and radius of x, y then we want them to move away from each other
        # Works but attraction ruins things
        try:
            x, y = bound_others
            if helper.distance(x, y) < (agent.radius*2 + x.radius + y.radius - 5):
                third_point = agent.pos + np.array([0, agent.radius])
                x_angle = helper.angle_on_cirumfrance(np.array(agent.pos), np.array(x.pos), np.array(third_point))
                y_angle = helper.angle_on_cirumfrance(np.array(agent.pos), np.array(y.pos), np.array(third_point))

                # Now they all circulate, but need to make them repel each other such that only two can be bound
                x_move_vec = x.pos + np.array([np.sin(x_angle + (np.pi/2)), np.cos(x_angle + (np.pi/2))])
                y_move_vec = y.pos + -np.array([np.sin(x_angle + (np.pi/2)), np.cos(x_angle + (np.pi/2))])
                x.pos = x_move_vec
                y.pos = y_move_vec
        except:
            return


    # For tests
    # Why does this work?
    def circulate(self, agent: agent.Agent) -> None:
        bound_others = [x for x in agent.model.agents if x is not agent and helper.distance(agent, x) <= (x.radius + agent.radius + self.strength)] 
        for x in bound_others:
            third_point = agent.pos + np.array([0, agent.radius])
            x_angle = helper.angle_on_cirumfrance(np.array(agent.pos), np.array(x.pos), np.array(third_point))
            x_move_vec = x.pos + np.array([np.sin(x_angle + (np.pi/2)), np.cos(x_angle + (np.pi/2))])
            x.pos = x_move_vec


    def step(self, agent: agent.Agent) -> None:
        """
            Checks if near agents have this behviour:
                -> If so, move closer to this agent (based on strength)
                -> Don't get stuck inside other agent
                -> If another agent is already attracted, be reuplsed to other side 
        """

        self.attract(agent, self.attracting_neighbours(agent)) 
        # self.attraction_constraints(agent)
        # self.circulate(agent)
        in_bounds(agent)

    
class Linking(Behaviour):
    """
        Linking class to make 'membranes'
    """
    def __init__(self) -> None:
        self.left = False
        self.right = False

    @staticmethod
    def links(agent: agent.Agent, angle: float) -> tuple[np.ndarray, np.ndarray]:
        centre = agent.pos
        _angle = (np.pi - angle)/2
        right = centre + np.array([agent.radius*np.cos(_angle), agent.radius*np.sin(_angle)])
        left = centre + np.array([agent.radius*np.cos(np.pi - _angle), agent.radius*np.sin(np.pi - _angle)])
        return right, left

    
    def link(self, agent: agent.Agent) -> None:
        if not self.right and (linking_neighs := [x for x in agent.model.agents if helper.distance_pos(x.pos, right_link := self.right_link(agent)) < x.radius]):
            print('Am here')
            linking_neigh = linking_neighs.pop()
            distance_vector = np.array(agent.pos) - np.array(right_link)
            move_vector = 0.1 * distance_vector
            agent.pos =  agent.pos - move_vector
            if (dist := helper.distance(agent, linking_neigh)) <= (agent.radius + linking_neigh.radius):
                overlap = 0.5 * (dist - agent.radius - linking_neigh.radius)
                agent.pos[0] -= overlap * (agent.pos[0] - linking_neigh.pos[0]) / dist
                agent.pos[1] -= overlap * (agent.pos[1] - linking_neigh.pos[1]) /dist
                linking_neigh.pos[0] += overlap * (agent.pos[0] - linking_neigh.pos[0]) / dist
                linking_neigh.pos[1] += overlap * (agent.pos[1] - linking_neigh.pos[1]) /dist
            
            self.right = True


    def step(self, agent: agent.Agent) -> None:
        self.link(agent)

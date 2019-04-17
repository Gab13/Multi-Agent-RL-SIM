# ------------------------------------------------------------------------------------------------------
# Gabriela Rivas
# ID: 201155263/u5gra
# Final Year Project 2018
# ------------------------------------------------------------------------------------------------------
# Random class for an agent. It finds and returns the next state the agent should go to based on
# random values.
# ------------------------------------------------------------------------------------------------------

from random import randint
from copy import copy, deepcopy
import World

class Random(object):

    state = 0
    initialState = 0
    totalStates = 0

    def __init__(self, width, height, initialState, world, agent):
        self.width = width
        self.height = height
        self.state = initialState
        self.initialState = initialState
        self.world = world
        self.agent = agent

        self.totalStates = self.width*self.height

        self.impassable = 4

        if agent == 1:
            self.objective = 5
        if agent == 2:
            self.objective = 1

    def move(self):
        self.random()

    # ------------------------------------------------------------------------------------------------------
    # MOVE TO A RANDOM REACHABLE STATE
    # ------------------------------------------------------------------------------------------------------
    def random(self):
        rand = randint(0, self.totalStates)

        while not self.reachable(self.state,rand) and not self.checkImpassable(rand):
            rand = randint(0, self.totalStates)

        nextState = rand

        self.world.updateGrid(nextState, self.agent)

        self.state = nextState

    # ------------------------------------------------------------------------------------------------------
    # Checking if a state is passable
    # ------------------------------------------------------------------------------------------------------
    def checkImpassable(self, r):
        count = 0
        for i in range(self.height):
            for j in range(self.width):
                if count == r:
                    if self.world.getGrid()[i][j] == self.impassable:
                        return False
                count+=1

    # ------------------------------------------------------------------------------------------------------
    # Checking if a state is reachable
    # ------------------------------------------------------------------------------------------------------
    def reachable(self, state, action):
        if state == action:
            return True
        elif state + self.width == action:
            return True
        elif state - self.width == action:
            return True
        else:
            if (state+1)%self.width == 0:
                if action == state-1:
                    return True
            elif(state)%self.width == 0:
                if action == state+1:
                    return True
            elif state+1 == action:
                return True
            elif state-1 == action:
                return True
            else: return False

    def getState(self):
        return self.state

    def getAgent(self):
        return self.agent

    # ------------------------------------------------------------------------------------------------------
    # Resetting the agent to it's original position
    # ------------------------------------------------------------------------------------------------------
    def resetState(self):
        self.state = self.initialState
        self.world.updateGrid(self.initialState, self.agent)

    def caughtHandling(self):
        pass

    def resetLearning(self):
        pass

    def getPolicy(self, state):
        return 0

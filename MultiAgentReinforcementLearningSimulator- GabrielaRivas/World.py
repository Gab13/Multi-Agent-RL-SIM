# ------------------------------------------------------------------------------------------------------
# Gabriela Rivas
# ID: 201155263/u5gra
# Final Year Project 2018
# ------------------------------------------------------------------------------------------------------
# World class. Manages the grid world for the agents and the objects in it. It is updated evry time
# an agent makes a move and checks whether any of the agents has reached it's objective.
# ------------------------------------------------------------------------------------------------------

#The world where the two agents will interact.
from copy import copy, deepcopy

class GridWorld:
    w = 0;
    h = 0;
    grid = None
    gridCopy = None
    gotReward = False

    def initialise(self, width, height, worldGrid):
        self.w = width
        self.h = height
        self.grid = [[0 for x in range(self.w)] for y in range(self.h)]

        self.grid = worldGrid
        self.gridCopy = deepcopy(worldGrid)

    def getGrid(self):
        return self.grid

    # ------------------------------------------------------------------------------------------------------
    # UPDATING THE GRID BASED ON THE STATE OF THE AGENT
    # ------------------------------------------------------------------------------------------------------
    def updateGrid(self,state, agent):
        count = 0
        finalObjective = 5
        temporaryObjective = 7
        pit = 6

        for i in range (self.h):
            for j in range(self.w):
                if self.gridCopy[i][j] == pit:
                    self.grid[i][j] = pit
                if self.gridCopy[i][j] == finalObjective and self.grid[i][j] != 2:
                    self.grid[i][j] = finalObjective
                if self.gridCopy[i][j] == temporaryObjective and self.grid[i][j] != 2 and self.gotReward == False:
                    self.grid[i][j] = temporaryObjective
                if count == state:
                    if self.gridCopy[i][j] == temporaryObjective and agent == 2:
                        self.grid[i][j] = 2
                    if self.gridCopy[i][j] == finalObjective and agent == 2:
                        self.grid[i][j] = 2
                    if self.gridCopy[i][j] == finalObjective and agent == 1:
                        self.grid[i][j] = finalObjective
                    if self.gridCopy[i][j] == temporaryObjective and agent == 1:
                        self.grid[i][j] = 1
                        self.gotReward = True
                    else:
                        self.grid[i][j] = agent

                if self.grid[i][j] == agent and count != state:
                    self.grid[i][j] = 0

                if self.gridCopy[i][j] == temporaryObjective and self.grid[i][j] != 2 and self.gotReward == False:
                    self.grid[i][j] = temporaryObjective
                if self.gridCopy[i][j] == finalObjective and self.grid[i][j] != 2:
                    self.grid[i][j] = finalObjective
                count += 1

    # ------------------------------------------------------------------------------------------------------
    # Resetting the grid to it's original state
    # ------------------------------------------------------------------------------------------------------
    def resetGrid(self):
        self.grid = deepcopy(self.gridCopy)
        self.gotReward = False

    def getCopy(self):
        return self.gridCopy

    # ------------------------------------------------------------------------------------------------------
    # Checking if the current state is the final state
    # ------------------------------------------------------------------------------------------------------
    def isFinalState(self, state, agent):
        count = 0;

        if agent == 1:
            self.objective = 5
        elif agent == 2:
            self.objective = 1

        for i in range(self.h):
            for j in range(self.w):
                if count == state:
                    if agent == 1 and self.getCopy()[i][j] == self.objective:
                        return True
                    elif agent == 2 and self.getGrid()[i][j] == self.objective:
                        return True
                    else:
                        return False
                count += 1
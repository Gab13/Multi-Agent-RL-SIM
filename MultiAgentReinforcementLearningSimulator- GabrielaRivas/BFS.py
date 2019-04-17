# ------------------------------------------------------------------------------------------------------
# Gabriela Rivas
# ID: 201155263/u5gra
# Final Year Project 2018
# ------------------------------------------------------------------------------------------------------
# Bredth First Search class for an agent. It finds and returns the next state the agent should go to based on
# the current shortest path path to its goal.
# ------------------------------------------------------------------------------------------------------

from random import randint
import World
import collections

# ---------------------------------------------------------
# BFS
# ---------------------------------------------------------
class shortestPath(object):
    impassable = 0
    objective = 0
    nextState = 0
    returnPolicy = False

    def __init__(self,width,height,initialState,world,agent):
        self.width = width
        self.height = height
        self.initialState = initialState
        self.world = world
        self.agent = agent

        self.impassable = 4

        if agent == 1:
            self.objective = 5
        if agent == 2:
            self.objective = 1

    def move(self):
        self.bfs()

    def getState(self):
        return self.nextState

    # ------------------------------------------------------------------------------------------------------
    # BREDTH FIRST SEARCH METHOD TO DETERMINE THE NEXT STATE FOR THE AGENT BASED ON
    # SHORTEST PATH TO IT'S OBJECTIVE
    # ------------------------------------------------------------------------------------------------------
    def bfs(self):
        start = self.getStartingPosition()
        grid = self.world.getGrid()

        queue = collections.deque([[start]])
        visited = set([start])
        while queue:
            route = queue.popleft()
            x, y = route[-1]
            if grid[y][x] == self.objective or (self.occupied() == True and grid[y][x] == 2):
                if self.returnPolicy == False:
                    self.nextState = self.getStateFromCoords(route[1])
                    self.world.updateGrid(self.nextState, self.agent)
                else:
                    return route
            for n in range (4):
                i, j = self.getNeighbor(x,y, n)
                if i < self.width and i >= 0 and j < self.height and j >= 0:
                    if grid[j][i] != self.impassable and (
                            i, j) not in visited:
                        queue.append(route + [(i, j)])
                        visited.add((i, j))

    def getNeighbor(self,x,y,count):
        if count == 0:
            return x,y+1
        if count == 1:
            return x,y-1
        if count == 2:
            return x+1,y
        if count == 3:
            return x-1,y

    # ------------------------------------------------------------------------------------------------------
    # Checking if the objective cell for agent 1 (5) is occupied by agent 2
    # ------------------------------------------------------------------------------------------------------
    def occupied(self):
        occupied = True
        if self.agent == 1:
            for i in range(self.height):
                for j in range(self.width):
                    if self.world.getGrid()[i][j] == 5:
                        occupied = False
        else: occupied = False

        return occupied

    def getAgent(self):
        return self.agent

    # ------------------------------------------------------------------------------------------------------
    # Getting a state number from coordinates x and y
    # ------------------------------------------------------------------------------------------------------
    def getStateFromCoords(self, coords):
        count = 0;
        state = 0;
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) == coords:
                    state = count
                count+=1
        return state

    # ------------------------------------------------------------------------------------------------------
    # Getting the position of the agent on the grid
    # ------------------------------------------------------------------------------------------------------
    def getStartingPosition(self):
        for i in range(self.height):
            for j in range (self.width):
                if self.world.getGrid()[i][j] == self.agent:
                    return (j,i)

    # ------------------------------------------------------------------------------------------------------
    # Resetting the agent to it's original position
    # ------------------------------------------------------------------------------------------------------
    def resetState(self):
        self.nextState = self.initialState
        self.world.updateGrid(self.initialState, self.agent)

    # ------------------------------------------------------------------------------------------------------
    # Returning the agent's steps
    # ------------------------------------------------------------------------------------------------------
    def getPolicy(self,state):
        self.returnPolicy = True
        route = self.bfs()
        self.returnPolicy = False
        return route

    def caughtHandling(self):
        pass
    def resetLearning(self):
        pass




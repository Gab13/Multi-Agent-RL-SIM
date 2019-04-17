# ------------------------------------------------------------------------------------------------------
# Gabriela Rivas
# ID: 201155263/u5gra
# Final Year Project 2018
# ------------------------------------------------------------------------------------------------------
# Qlearning class for an agent. It finds and returns the next state the agent should go to based on
# it's learning matrix and random values every 'epsilon' probability. It also returns the current agent
# policy based on it's learning up to a point.
# ------------------------------------------------------------------------------------------------------

from random import randint
from copy import copy, deepcopy
import World

class Qlearning(object):
    i = j = 0;

    totalStates = 0;
    enemy = 0;

    reward = 5;
    rewardObjective1 = 10;
    impassable = -1;
    catch = -100;
    defaultReward = 0;
    pit = -20;
    caught = False;
    previousState = 0;
    epsilon = 0;

    def __init__(self, width, height, startingState, world, agent, alpha, gamma, epsilon):

        self.width = width
        self.height = height
        self.startingState = startingState
        self.world = world
        self.agent = agent
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.state = self.startingState
        self.totalStates= self.width * self.height;

        if self.agent == 1:
            self.objective = 5;
            self.enemy = 2
        if self.agent == 2:
            self.objective = 1;
            self.enemy = None


        self.RewardsMatrix = [[0 for x in range(self.totalStates)] for y in range(self.totalStates)]
        self.QLearning = [[0 for x in range(self.totalStates)] for y in range(self.totalStates)]

        self.updateRMatrix()

    # ------------------------------------------------------------------------------------------------------
    # SETTING UP THE REWARD VALUES
    # ------------------------------------------------------------------------------------------------------
    def updateRMatrix(self):

        #Initialise the grid
        grid = self.world.getGrid()

        #Initialise the rewards matrix with -1 (Impassable)
        for i in range(self.totalStates):
            for j in range(self.totalStates):
                self.RewardsMatrix[i][j] = -1

        for state in range(self.totalStates):
            for action in range(self.totalStates):

                if self.reachable(state,action):
                    if self.getCellFromState(action) == self.enemy:
                        self.RewardsMatrix[state][action] = self.catch
                    elif self.getCellFromState(action) == self.objective:
                        self.RewardsMatrix[state][action] = self.reward
                    elif self.getCellFromState(action) == 6:
                        self.RewardsMatrix[state][action] = self.pit
                    elif self.getCellFromState(action) == 4:
                        self.RewardsMatrix[state][action] = self.impassable
                    elif self.getCellFromState(action) == 7 and self.getAgent()==1:
                        self.RewardsMatrix[state][action] = self.rewardObjective1
                    else:
                        self.RewardsMatrix[state][action] = 0

    def getCellFromState(self, action):
        count = 0

        for i in range(self.height):
            for j in range(self.width):
                if count == action:
                    return self.world.getGrid()[i][j]
                count+=1

    # ------------------------------------------------------------------------------------------------------
    # Checking if an action is possible from a given state
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

    # ------------------------------------------------------------------------------------------------------
    # Resseting the agent to its initial position
    # ------------------------------------------------------------------------------------------------------
    def resetState(self):
        self.state = self.startingState
        self.world.updateGrid(self.state, self.agent)

    def resetLearning(self):
        self.updateRMatrix()

    def getAgent(self):
        return self.agent

    def setCaught(self,c):
        self.caught = c

    def move(self):
        self.calculateQ()

    # ------------------------------------------------------------------------------------------------------
    # Method to hande what happens when the agent gets caught
    # ------------------------------------------------------------------------------------------------------
    def caughtHandling(self):
        #print("caught")
        #print(self.state)
        self.setCaught(True)
        self.updateRMatrix()
        self.calculateQ()  # Learning algorithm
        self.setCaught(False)
        #self.printQMatrix()
        #print("")

    # ------------------------------------------------------------------------------------------------------
    # TEMPORAL DIFFERENCE QLEARNING ALGORITHM
    # ------------------------------------------------------------------------------------------------------
    def calculateQ(self):

        if self.caught == True:
            nextState = deepcopy(self.state)
            self.state = deepcopy(self.previousState)
        else:
            # Select state with max reward value reachable from current state.
            nextState = self.maxState(self.state)
            self.previousState = deepcopy(self.state)

        maxQ = self.maxQ(nextState)

        r = self.RewardsMatrix[self.state][nextState]

        q = self.QLearning[self.state][nextState]

        tmp = q + self.alpha * (r + self.gamma * maxQ - q);

        self.QLearning[self.state][nextState] = tmp

        if self.caught != True:
            self.world.updateGrid(nextState, self.agent)  # Updating the positions of the agents on the grid
            self.state = nextState
            self.updateRMatrix()

    # ------------------------------------------------------------------------------------------------------
    # Getting the state of the other agent (used for debug)
    # ------------------------------------------------------------------------------------------------------
    def getEnemyState(self):
        state = 0

        for i in range(self.height):
            for j in range(self.width):
                if self.world.getGrid()[i][j] == self.enemy:
                    return state
                state += 1

    # ------------------------------------------------------------------------------------------------------
    # Checking the possible actions a state can take (based on wether they are passable)
    # ------------------------------------------------------------------------------------------------------
    def possibleActionsFromState(self,state):
        result = []
        for i in range(self.totalStates):
            if self.RewardsMatrix[state][i] != -1:
                result.append(i)
        return result

    # ------------------------------------------------------------------------------------------------------
    # Method to print the rewards matrix(debug)
    # ------------------------------------------------------------------------------------------------------
    def printR(self):
        for i in range(self.totalStates):
            for j in range(self.totalStates):
                print(self.RewardsMatrix[i][j], " ", end = "")
            print("")

    # ------------------------------------------------------------------------------------------------------
    #  Choosing a state to go to based on it's max q value and
    #  epsilon greedy policy.
    # ------------------------------------------------------------------------------------------------------
    def maxState(self, state):
        equalActions = []

        possibleActions = self.possibleActionsFromState(state)

        #Only 1 possible action check
        if len(possibleActions) == 1:
            maxState = possibleActions[0]
        else:
            # Probability of exploring a new state(without maxQ)
            tmp = randint(0, 100)
            if tmp < self.epsilon:
                tmp = randint(0, len(possibleActions) - 1)
                maxState = possibleActions[tmp]
            else:
                maxValue = 0
                maxState = 0

                count = 0

                for count in range(len(possibleActions)):
                    value = self.QLearning[state][possibleActions[count]]

                    if count == 0:
                        maxValue = value

                    if value >= maxValue:
                        maxState = possibleActions[count]
                        maxValue = value

                count = 0

                for count in range(len(possibleActions)):
                    value = self.QLearning[state][possibleActions[count]]

                    if value == maxValue:
                        equalActions.append(possibleActions[count])

                if len(equalActions) != 1:
                    tmp = randint(0, len(equalActions) - 1)
                    maxState = equalActions[tmp]
                else:
                    maxState = equalActions[0]

        return maxState

    # ------------------------------------------------------------------------------------------------------
    # Returning the max q value of a state
    # ------------------------------------------------------------------------------------------------------
    def maxQ(self, nextState):

        possibleActions = self.possibleActionsFromState(nextState)
        maxValue = 0

        for count in range(len(possibleActions)):
            value = self.QLearning[nextState][possibleActions[count]]

            if value > maxValue:
                maxValue = value

        return maxValue

    # ------------------------------------------------------------------------------------------------------
    # Printing the Q Learning Matrix (Debug)
    # ------------------------------------------------------------------------------------------------------
    def printQMatrix(self):
        print("")
        print("Q matrix")
        for i in range (len(self.QLearning)):
            print(self.QLearning[i])
        print("")

    def getCoordsFromState(self,state):
        count = 0

        for i in range(self.height):
            for j in range(self.width):
                if count == state:
                    return i, j
                count += 1

    # ------------------------------------------------------------------------------------------------------
    # METHOD THAT RETURNS THE POLICY OF THE AGENT
    # ------------------------------------------------------------------------------------------------------
    # The policy is returned as a random set of values towards the goal (in the same manner as the
    # agent searches for it) if it hasn't yet developed a concrete strategy to reach it.
    # ------------------------------------------------------------------------------------------------------
    def getPolicy(self,state):
        maxValue = 0;
        nextState = 0;
        finalRoute = []

        while self.world.isFinalState(state, self.agent) == False:
            possibleActions = self.possibleActionsFromState(state)
            equalActions = []

            finalRoute.append(self.getCoordsFromState(state))

            for i in range(len(possibleActions)):
                value = self.QLearning[state][possibleActions[i]]

                if value >= maxValue:
                    maxValue = value
                    equalActions.append(possibleActions[i])

                if len(equalActions) > 1:
                    tmp = randint(0,len(equalActions) - 1)
                    nextState = equalActions[tmp]
                else: nextState = possibleActions[i]

            state = nextState

        return finalRoute








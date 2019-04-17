Multi-Agent Reinforcement Learning Simulator
Gabriela Rivas
201155263
——————————————————————————————————————————————————————
Program Requirements:

Libraries to be installed:
Pygame - https://www.pygame.org/news
Matplot - https://matplotlib.org/

Mac OSX 64 bit. 
——————————————————————————————————————————————————————
Inserting new algorithms:

1 - Name each method accordingly.

Obligatory:
    move(): — Needs to makes use of the ‘World.py’ method ‘updateGrid(state,agent)’ to move the agent to a new state.
    resetState(): - Sets the agent back to it’s original state.
    getState(): Returns the current state of the agent.
Optional:
    resetLearning(): - Restarts an agent’s learning.
    getPolicy(): Returns the current path the agent’s taking
    caughtHandling(): In case something is to be done after agent 1 is caught
Main Callable Method:
    isFinalState(state, agent): - Method from the ‘World.py’ class. Checks wether the agent has reached it’s objective.

If not using the optional methods, set them in the algorithm but leave them blanch by calling ‘pass’.


2 - Initialise the algorithm at the top of the ‘Controller class’:

    1 - Add initialisation for the algorithm with the desired values and add an if statement with the name of the algorithm
        as shown on the examples below.
    2 - Add the name of the algorithm onto the list of algorithms to be able to select it from the interface




    # -----------------------------------------------------------------------------------------------------
    # LIST OF ALGORITHMS [EDITABLE]
    # -----------------------------------------------------------------------------------------------------
    currentAlgorithms = ["Qlearning", "BFS", "Random"] #Add the name of an algorithm to insert it into the list

    algorithmAgent1 = algorithmAgent2 = "Qlearning" #Default algorithm for both agents

    # -----------------------------------------------------------------------------------------------------
    # INITIALISATION OF THE AGENTS [EDITABLE]
    # -----------------------------------------------------------------------------------------------------
    # Add the initialisation for the algorithm
    # -----------------------------------------------------------------------------------------------------
    def initialiseAgents(self):

        if self.active_agent_1 == True:
            if self.algorithmAgent1 == "Qlearning":
                self.agent1 = Qlearn.Qlearning(self.width, self.height, self.initState1, self.world, 1,
                                               self.alphaAgent1, self.gammaAgent1, self.epsilonAgent1)
            if self.algorithmAgent1 == "BFS":
                self.agent1 = BFS.shortestPath(self.width, self.height, self.initState1, self.world, 1)

            if self.algorithmAgent1 == "Random":
                self.agent1 = Random.Random(self.width, self.height, self.initState1, self.world, 1)

        if self.active_agent_2 == True:
            if self.algorithmAgent2 == "Qlearning":
                self.agent2 = Qlearn.Qlearning(self.width, self.height, self.initState2, self.world, 2,
                                               self.alphaAgent2, self.gammaAgent2, self.epsilonAgent2)
            if self.algorithmAgent2 == "BFS":
                self.agent2 = BFS.shortestPath(self.width, self.height, self.initState2, self.world, 2)

            if self.algorithmAgent2 == "Random":
                self.agent2 = Random.Random(self.width, self.height, self.initState2, self.world, 2)



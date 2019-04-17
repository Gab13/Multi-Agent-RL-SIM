# ------------------------------------------------------------------------------------------------------
# Gabriela Rivas
# ID: 201155263/u5gra
# Final Year Project 2018
# ------------------------------------------------------------------------------------------------------
# Control and Interface classes. The Control class initialises the Interface class.
# The Interface class sets default values for the variables and initialises the GUI in Tkinter for
# prompting of customised worlds and values. It also initialises the simulation in Pygame.
# ------------------------------------------------------------------------------------------------------

import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import pygame
import Qlearn
import BFS
import Random
import World
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np

class Interface():
    # -----------------------------------------------------------------------------------------------------
    # INITIALISATION OF VARIABLES
    # -----------------------------------------------------------------------------------------------------

    #To do with agent and score initialisation
    main = None
    agent1 = agent2 = None
    active_agent_1 = active_agent_2 = False
    agent1Progress = agent2Progress = []
    count = ag1TotalWins = ag2TotalWins = ag1Wins = ag2Wins = 0
    initState1 = initState2 = 0

    # To do with simulation control
    speed_of_simulation = 10
    startOver = True
    display = True
    pause = False
    iterations = 0
    number_of_iterations = 10000

    #To do with grid control
    worldGrid = []
    width = height = 0;
    worldGrid_Entry = None
    world = World.GridWorld();

    #To do with learning parameters
    alphaAgent1 = alphaAgent2 = 0.9
    gammaAgent1 = gammaAgent2 = 0.1
    epsilonAgent1 = epsilonAgent2 = 20
    graphSettings = 50
    agent1StepCount = agent2StepCount = []

    alpha_agent_1_Entry = alpha_agent_2_Entry = gamma_agent_1_Entry = gamma_agent_2_Entry \
        = graphBtn = iterations_Entry = speed_of_simulation_Entry = epsilon_1_Entry = \
        epsilon_2_Entry = algorithmBtn = policyBtn= graphAg1Btn=None

    #To do with grid from text file setup
    mFromFile = False
    file = None

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

    # ------------------------------------------------------------------------------------------------------
    # SET DEFAULT MATRIX [EDITABLE]
    # ------------------------------------------------------------------------------------------------------
    def setDefaultMatrix(self):
        defaultMatrix = ['1','0','0','0','\n','2','0','0','0','\n','0','4','4','0','\n','0','0','0','5','\n']

        return defaultMatrix

    # ------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------


    # Do not edit past this point --------------------------------------------------------------------------


    # ------------------------------------------------------------------------------------------------------
    # INITIALISATION OF THE ALGORITHM
    # ------------------------------------------------------------------------------------------------------
    def initialiseAlgorithm(self):

        initState1 = 0
        initState2 = 0

        self.world.initialise(self.width, self.height, self.worldGrid)

        self.count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.worldGrid[i][j] == 1:
                    self.initState1 = self.count
                    self.active_agent_1 = True
                if self.worldGrid[i][j] == 2:
                    self.initState2 = self.count
                    self.active_agent_2 = True
                self.count += 1

        self.initialiseAgents()

        self.agent1Progress = []
        self.agent2Progress = []
        self.ag1Wins = self.ag2Wins = self.ag1TotalWins = self.ag2TotalWins = self.count = 0

        # Set the display of the wins for each agent
        winsDisplay = ''
        winsDisplay = winsDisplay + "Score: agent 1:(" + str(self.ag1TotalWins) + ") agent 2:(" + str(
            self.ag2TotalWins) + ") Total:(" + str(self.ag1TotalWins + self.ag2TotalWins) + ")"
        pygame.display.set_caption(winsDisplay)

        self.startOver = False

    # ------------------------------------------------------------------------------------------------------
    # GUI FOR THE MAIN MENU
    # ------------------------------------------------------------------------------------------------------
    def startup(self):
        self.main = tk.Tk()
        self.main.title('Simulation')
        self.main.geometry('300x650')
        self.main.resizable(False,False)

        # create button to open file
        instructionsBtn = tk.Button(self.main, text='Instructions', command=self.displayInstructions)
        instructionsBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        worldGridText = 'Insert world Matrix:'
        worldGridLabel = Label(self.main, text=worldGridText)
        worldGridLabel.pack()
        self.worldGrid_Entry = Text(self.main, height=10, width=10)
        self.worldGrid_Entry.focus_set()
        self.worldGrid_Entry.pack()

        instructionsBtn = tk.Button(self.main, text='Open matrix from txt file', command=self.matrixFromFile)
        instructionsBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        self.algorithmBtn = tk.Button(self.main, text='Choose algorithm', command=self.chooseLearningAlgorithm)
        self.algorithmBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        iterations_text = 'Set number of iterations to perform:'
        iterations_Label = Label(self.main, text=iterations_text)
        iterations_Label.pack()
        self.iterations_Entry = Entry(self.main, width=15)
        self.iterations_Entry.focus_set()
        self.iterations_Entry.pack()

        divisorText = ' ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(self.main, text=divisorText, height=1)
        divisorLabel.pack()
        startBtn = tk.Button(self.main, text='Start Simulation', command=self.setup)
        startBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)
        divisorText = ' ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(self.main, text=divisorText, height=1)
        divisorLabel.pack()

        speed_of_simulation_text = 'Speed of simulation (1 = fastest):'
        speed_of_simulation_Label = Label(self.main, text=speed_of_simulation_text)
        speed_of_simulation_Label.pack()
        self.speed_of_simulation_Entry = Entry(self.main, width=4)
        self.speed_of_simulation_Entry.focus_set()
        self.speed_of_simulation_Entry.pack()

        self.graphBtn = tk.Button(self.main, text='View Progress Graph (both agents)', command=self.viewGraph)
        self.graphBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)
        self.graphBtn.configure(state='disabled')

        self.graphAg1Btn = tk.Button(self.main, text='View Progress agent 1', command=self.viewGraphAgent1)
        self.graphAg1Btn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)
        self.graphAg1Btn.configure(state='disabled')

        restartBtn = tk.Button(self.main, text='Reset', command=self.reset)
        restartBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        self.policyBtn = tk.Button(self.main, text='View Policies', command=self.viewPolicies)
        self.policyBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)
        self.policyBtn.configure(state='disabled')

        settingsBtn = tk.Button(self.main, text='Settings', command=self.openSettings)
        settingsBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        quitBtn = tk.Button(self.main, text='Quit', command=self.main.quit)
        quitBtn.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        self.main.mainloop()

    # ------------------------------------------------------------------------------------------------------
    # GUI FOR THE SETTINGS MENU
    # ------------------------------------------------------------------------------------------------------

    def openSettings(self):
        settings_window = tk.Toplevel(self.main)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.resizable(False, False)

        displayTrue = tk.Button(settings_window, text='Simulation OFF', command=self.changeDisplayFalse)
        displayTrue.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        displayFalse = tk.Button(settings_window, text='Simulation ON', command=self.changeDisplayTrue)
        displayFalse.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

        graphSettings_text = 'Iterations per unit (for the graph):'
        graphSettings_Label = Label(settings_window, text=graphSettings_text)
        graphSettings_Label.pack()
        self.graphSettings_Entry = Entry(settings_window, width=4)
        self.graphSettings_Entry.focus_set()
        self.graphSettings_Entry.pack()

        setValue = tk.Button(settings_window, text='Set this value', command=self.setSettingsValue)
        setValue.pack(expand=tk.FALSE, fill=tk.X, side=tk.TOP)

    def setSettingsValue(self):
        tmp = self.graphSettings_Entry.get()
        try:
            self.graphSettings = float(tmp)
        except ValueError:
            self.graphSettings = 50

    # Method to read input from a txt file
    def matrixFromFile(self):
        self.file = askopenfilename()
        self.mFromFile = True


    # Activate the simulation
    def changeDisplayTrue(self):
        self.display = True

    # Deactivate the simulation
    def changeDisplayFalse(self):
        self.display = False

    # ------------------------------------------------------------------------------------------------------
    # GUI FOR THE 'CHOOSE ALGORITHM' OPTION
    # ------------------------------------------------------------------------------------------------------
    def chooseLearningAlgorithm(self):

        algorithm_window = tk.Toplevel(self.main)
        algorithm_window.title("Choose algorithm")
        algorithm_window.geometry("400x790")
        algorithm_window.resizable(False, False)

        divisorText = '            '
        divisorLabel = Label(algorithm_window, text=divisorText, height=1)
        divisorLabel.pack()

        listbox = Listbox(algorithm_window)
        listbox.pack()

        for item in self.currentAlgorithms:
            listbox.insert(END, item)

        algorithmText = 'Current algorithm agent 1: ' + self.algorithmAgent1
        algorithmLabel = Label(algorithm_window, text=algorithmText)
        algorithmLabel.pack()

        algorithmText2 = 'Current algorithm agent 2: ' + self.algorithmAgent2
        algorithmLabel2 = Label(algorithm_window, text=algorithmText2)
        algorithmLabel2.pack()

        chooseBtn = Button(algorithm_window, text="Choose for Agent 1",
                   command=lambda listbox=listbox: self.setLearningAlgorithm(listbox.get(ANCHOR),algorithmLabel,1))
        chooseBtn.pack()

        chooseBtn = Button(algorithm_window, text="Choose for Agent 2",
                           command=lambda listbox=listbox: self.setLearningAlgorithm(listbox.get(ANCHOR),
                                                                                     algorithmLabel2,2))
        chooseBtn.pack()

        divisorText = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(algorithm_window, text=divisorText, height=1)
        divisorLabel.pack()

        divisorText = 'Insert the alpha and gamma values for agents 1 and 2'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        divisorText = 'alpha--learning rate(0-1), gamma--discount reward rate(0-1)'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        divisorText = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        alpha_agent_1_text = 'Insert alpha for agent 1:'
        alpha_agent_1_Label = Label(algorithm_window, text=alpha_agent_1_text)
        alpha_agent_1_Label.pack()
        self.alpha_agent_1_Entry = Entry(algorithm_window, width=4)
        self.alpha_agent_1_Entry.focus_set()
        self.alpha_agent_1_Entry.pack()

        alpha_agent_2_text = 'Insert alpha for agent 2:'
        alpha_agent_2_Label = Label(algorithm_window, text=alpha_agent_2_text)
        alpha_agent_2_Label.pack()
        self.alpha_agent_2_Entry = Entry(algorithm_window, width=4)
        self.alpha_agent_2_Entry.focus_set()
        self.alpha_agent_2_Entry.pack()

        gamma_agent_1_text = 'Insert gamma for agent 1:'
        gamma_agent_1_Label = Label(algorithm_window, text=gamma_agent_1_text)
        gamma_agent_1_Label.pack()
        self.gamma_agent_1_Entry = Entry(algorithm_window, width=4)
        self.gamma_agent_1_Entry.focus_set()
        self.gamma_agent_1_Entry.pack()

        gamma_agent_2_text = 'Insert gamma for agent 2:'
        gamma_agent_2_Label = Label(algorithm_window, text=gamma_agent_2_text)
        gamma_agent_2_Label.pack()
        self.gamma_agent_2_Entry = Entry(algorithm_window, width=4)
        self.gamma_agent_2_Entry.focus_set()
        self.gamma_agent_2_Entry.pack()

        divisorText = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        divisorText = 'Insert epsilon (Probability 0 - 100 of exploring new states)'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        divisorText = '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'
        divisorLabel = Label(algorithm_window, text=divisorText)
        divisorLabel.pack()

        epsilon_1_text = 'Epsilon for agent 1:'
        epsilon_1_Label = Label(algorithm_window, text=epsilon_1_text)
        epsilon_1_Label.pack()
        self.epsilon_1_Entry = Entry(algorithm_window, width=4)
        self.epsilon_1_Entry.focus_set()
        self.epsilon_1_Entry.pack()

        epsilon_2_text = 'Epsilon for agent 2:'
        epsilon_2_Label = Label(algorithm_window, text=epsilon_2_text)
        epsilon_2_Label.pack()
        self.epsilon_2_Entry = Entry(algorithm_window, width=4)
        self.epsilon_2_Entry.focus_set()
        self.epsilon_2_Entry.pack()

        setValuesBtn = Button(algorithm_window, text="Set these values",
                              command=lambda listbox=listbox: self.setAlgorithmValues(algorithm_window))
        setValuesBtn.pack()

    # ------------------------------------------------------------------------------------------------------
    # METHOD TO SET THE ALGORITHM VALUES FROM THE ENTRIES
    # ------------------------------------------------------------------------------------------------------
    def setAlgorithmValues(self, algorithm_window):

        tmp = self.alpha_agent_1_Entry.get()
        try:
            self.alphaAgent1 = float(tmp)
        except ValueError:
            self.alphaAgent1 = 0.1

        tmp = self.alpha_agent_2_Entry.get()
        try:
            self.alphaAgent2 = float(tmp)
        except ValueError:
            self.alphaAgent2 = 0.1

        tmp = self.gamma_agent_1_Entry.get()
        try:
            self.gammaAgent1 = float(tmp)
        except ValueError:
            self.gammaAgent1 = 0.9

        tmp = self.gamma_agent_2_Entry.get()
        try:
            self.gammaAgent2= float(tmp)
        except ValueError:
            self.gammaAgent2 = 0.9

        tmp = self.epsilon_1_Entry.get()
        try:
            self.epsilonAgent1= float(tmp)
        except ValueError:
            self.epsilonAgent1 = 20

        tmp = self.epsilon_2_Entry.get()
        try:
            self.epsilonAgent2 = float(tmp)
        except ValueError:
            self.epsilonAgent2 = 20

        Text = 'Values set'
        confirmationLabel = Label(algorithm_window, text=Text, height=1)
        confirmationLabel.pack()

    # ------------------------------------------------------------------------------------------------------
    # Method to set the learning algorithm for each agent
    # ------------------------------------------------------------------------------------------------------
    def setLearningAlgorithm(self, algorithm, algorithmLabel,agent):

        if algorithm != "":
            if agent == 1:
                self.algorithmAgent1 = algorithm
            elif agent == 2:
                self.algorithmAgent2 = algorithm

        algorithmText = 'Current algorithm agent ' + str(agent) + ': ' + algorithm
        algorithmLabel.config(text=algorithmText)
        algorithmLabel.pack()

    # ------------------------------------------------------------------------------------------------------
    # STARTTING UP THE WORLD MATRIX AND THE VALUES BASED ON THE ENTRIES
    # AND INITIALISING THE SIMULATION
    # ------------------------------------------------------------------------------------------------------
    def setup(self):
        matrix = []

        #To make the speed of simulation editable at pause
        if self.pause == True or self.startOver == True:
            tmp = self.speed_of_simulation_Entry.get()
            try:
                self.speed_of_simulation = int(tmp)
            except ValueError:
                self.speed_of_simulation = 10
            self.pause = False

        # Obtaining the matrix and set values
        if self.pause == False or self.startOver == True:
            self.iterations = 0

            tmp = self.iterations_Entry.get()
            try:
                self.number_of_iterations = int(tmp)
            except ValueError:
                self.number_of_iterations = 100000000

            # Check if a file has been chosen
            if self.mFromFile == False:
                tmp = self.worldGrid_Entry.get(1.0, END)
                matrix = list(tmp)
            else:
                with open(self.file) as fileobj:
                    for line in fileobj:
                        for ch in line:
                            matrix.append(ch)
                matrix.append('\n')

            if matrix == ['\n']:
                matrix = self.setDefaultMatrix()

            # Setting up the matrix
            self.width = 0
            self.height = 0
            i = 0
            numberCount = 0
            length = len(matrix)

            while i < length:
                if matrix[i] == '\n':
                    i = length + 1
                else:
                    self.width += 1
                i += 1

            for i in range(length):
                if matrix[i] == '\n':
                    self.height += 1

            self.worldGrid = [[0 for x in range(self.width)] for y in range(self.height)]

            for i in range(self.height):
                for j in range(self.width):
                    if matrix[numberCount] != '\n':
                        self.worldGrid[i][j] = int(matrix[numberCount])
                    numberCount += 1
                numberCount += 1

            self.worldGrid_Entry.configure(state='disabled')
            self.iterations_Entry.configure(state='disabled')


        self.policyBtn.configure(state='normal')
        self.algorithmBtn.configure(state='disabled')

        #Initialise the simulation
        self.initSimulation()

    # ------------------------------------------------------------------------------------------------------
    # Resetting the simulation
    # ------------------------------------------------------------------------------------------------------
    def reset(self):
        self.worldGrid_Entry.configure(state='normal')
        self.iterations_Entry.configure(state='normal')
        self.graphBtn.configure(state='disabled')
        self.policyBtn.configure(state='disabled')
        self.algorithmBtn.configure(state='normal')
        self.graphAg1Btn.configure(state='disabled')
        self.startOver = True
        self.active_agent_1 = False
        self.active_agent_2 = False
        self.mFromFile = False
        self.agent1StepCount = []
        pygame.quit()


    # ------------------------------------------------------------------------------------------------------
    # DISPLAY FOR THE SIMULATION
    # ------------------------------------------------------------------------------------------------------
    def initSimulation(self):
        tileWidth = 60 - self.width
        tileHeight = 60 - self.width
        separation = 5

        pygame.init()

        white = (255, 255, 255)
        black = (0, 0, 0)
        blue = (0, 0, 255)
        red = (255, 0, 0)
        green = (0, 255, 0)
        grey = (100, 100, 100)
        yellow= (255, 255, 0)

        screenSize = [100 * self.width, 85 * self.height]
        screen = pygame.display.set_mode(screenSize)

        font = pygame.font.Font(pygame.font.get_default_font(), 12)

        #Creating the Pause button
        screen.fill(black)
        stopButton = pygame.Rect(70 * self.width, 55 * self.height, 50, 20)
        pygame.draw.rect(screen, white, stopButton)  # draw button

        stopNowButton = pygame.Rect(70 * self.width, 40 * self.height, 70, 20)
        pygame.draw.rect(screen, white, stopNowButton)  # draw button

        pauseText = font.render("   Pause", True, black)
        screen.blit(pauseText, [70 * self.width, 55 * self.height])
        pygame.display.flip()

        pauseNowText = font.render("Pause Now", True, black)
        screen.blit(pauseNowText, [70 * self.width, 40 * self.height])
        pygame.display.flip()

        finished = self.pause = False

        # ---------------------------------------------------------------------------------------
        # GRID DISPLAY
        # ---------------------------------------------------------------------------------------
        while not finished:

            if self.startOver == True:
                # Initialise the agents
                self.initialiseAlgorithm()
                #self.agent1.printR() #debug

            # ------------------------------------------------------------------------------------
            while self.iterations < self.number_of_iterations and not finished:
                steps = 0

                if self.active_agent_1:
                    self.agent1.resetState()  # Common method for all learning classes, reset to the original position
                if self.active_agent_2:
                    self.agent2.resetState()

                if self.active_agent_1:
                    if self.active_agent_1:
                        self.agent1.resetLearning()
                if self.active_agent_1:
                    if self.active_agent_2:
                        self.agent2.resetLearning()

                # While no agent has reached its final state or agent 1 hasn't gotten caught
                while self.finishIterating() is False and not finished:

                    grid = self.world.getGrid()

                    if self.display == True:
                        screen.fill(black)
                        pygame.draw.rect(screen, white, stopButton)
                        screen.blit(pauseText, [70 * self.width, 55 * self.height])

                        pygame.draw.rect(screen, white, stopNowButton)
                        screen.blit(pauseNowText, [70 * self.width, 40 * self.height])

                        for i in range(self.height):
                            for j in range(self.width):
                                colour = white
                                if grid[i][j] == 5:
                                    colour = green
                                elif grid[i][j] == 1:
                                    colour = blue
                                elif grid[i][j] == 6:
                                    colour = grey
                                elif grid[i][j] == 4:
                                    colour = black
                                elif grid[i][j] == 2:
                                    colour = red
                                elif grid[i][j] == 7:
                                    colour = yellow
                                pygame.draw.rect(screen, colour, [(separation +tileWidth) * j + separation,
                                                                  (separation + tileHeight) * i + separation,
                                                                  tileWidth, tileHeight])

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.pause = True
                            finished = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos  # gets mouse position

                            if stopButton.collidepoint(mouse_pos):
                                self.pause = True
                            if stopNowButton.collidepoint(mouse_pos):
                                self.pause = True
                                finished = True

                    pygame.display.flip()
                    pygame.time.wait(self.speed_of_simulation)

                    # Activate the algorithm's learning method
                    # ----------------------------------------------
                    if self.active_agent_1:
                        self.agent1.move()  # Movement
                    if self.active_agent_2 and self.gotCaught() == False:
                        self.agent2.move();  # Movement
                    if self.gotCaught() == True:
                        self.world.updateGrid(self.agent2.getState(), 2)

                    steps+=1

                if self.active_agent_1 and not self.active_agent_2 and self.pause == False:
                    self.agent1StepCount.append(steps)

                # Every learning algorithm class must have a method (isFinalState()) which returns True if
                # The agent has reached it's desired location
                if self.gotCaught() == True and self.active_agent_2:
                    self.ag2TotalWins += 1
                    self.ag2Wins += 1
                elif self.active_agent_1:
                    self.ag1TotalWins += 1
                    self.ag1Wins += 1

                if self.gotCaught() == True:
                    self.agent1.caughtHandling()

                self.count += 1

                #ITERATIONS PER UNIT = 50 (default) FOR GRAPH
                if self.count == self.graphSettings and self.pause == False:
                    self.agent1Progress.append(self.ag1Wins)
                    self.agent2Progress.append(self.ag2Wins)
                    self.ag2Wins = 0
                    self.ag1Wins = 0
                    self.count = 0

                if self.pause == True:
                    self.ag1Wins = 0
                    self.ag2Wins = 0
                    self.count = 0

                winsDisplay = ''
                winsDisplay = winsDisplay + "Score: agent 1:(" + str(self.ag1TotalWins) + ") agent 2:(" + str(
                    self.ag2TotalWins) + ") Total:(" + str(self.ag1TotalWins + self.ag2TotalWins) + ")"
                pygame.display.set_caption(winsDisplay)

                self.world.resetGrid()
                self.iterations += 1

                if self.pause == True:
                    if self.active_agent_1 and self.active_agent_2:
                        self.graphBtn.configure(state='normal')
                    if self.active_agent_1 and not self.active_agent_2:
                        self.graphAg1Btn.configure(state='normal')
                    finished = True

            self.pause = True
            if self.active_agent_1 and self.active_agent_2:
                self.graphBtn.configure(state='normal')
            finished = True


    # ------------------------------------------------------------------------------------------------------
    # Method to check whether either agent has reached its objective
    # ------------------------------------------------------------------------------------------------------
    def finishIterating(self):

        if self.active_agent_1 and self.active_agent_2:
            if self.world.isFinalState(self.agent1.getState(), 1) is False and self.world.isFinalState(
                    self.agent2.getState(), 2) is False \
                    and self.gotCaught() is False:
                return False
            else:
                return True

        if self.active_agent_1 and not self.active_agent_2:
            if self.world.isFinalState(self.agent1.getState(), 1) is False:
                return False
            else:
                return True

        if self.active_agent_2 and not self.active_agent_1:
            if self.world.isFinalState(self.agent2.getState(), 2) is False:
                return False
            else:
                return True

    # ------------------------------------------------------------------------------------------------------
    #  Method to check if agent 1 has gotten caught by agent 2
    # ------------------------------------------------------------------------------------------------------
    def gotCaught(self):
        if self.active_agent_1 and self.active_agent_2:
            if self.agent1.getState() == self.agent2.getState():
                return True
            else:
                return False

    # ------------------------------------------------------------------------------------------------------
    #  Method that prints the policies for each agent
    # ------------------------------------------------------------------------------------------------------
    def viewPolicies(self):
        policies_window = tk.Toplevel(self.main)
        policies_window.title("Current Policies")

        policiesText = Text(policies_window, height=10, width=80)
        policiesText.pack()

        if self.active_agent_1:
            policyAgent1 = self.agent1.getPolicy(self.initState1)
            text = ''.join(str(e) for e in policyAgent1)
            policiesText.insert(END,"Policy agent 1: " + text)
        if self.active_agent_2:
            policyAgent2 = self.agent2.getPolicy(self.initState2)
            text = ''.join(str(e) for e in policyAgent2)
            policiesText.insert(END,"\n\nPolicy agent 2: " + text)


    # ------------------------------------------------------------------------------------------------------
    # Instructions panel
    # ------------------------------------------------------------------------------------------------------
    def displayInstructions(self):
        instructions_window = tk.Toplevel(self.main)
        instructions_window.title("Instructions")
        instructions_window.resizable(False, False)

        instructions_frame = tk.Frame(instructions_window, width=30, height=120)
        instructions_frame.pack(fill="both", expand=True)

        instructions_frame.grid_propagate(False)
        # implement stretchability
        instructions_frame.grid_rowconfigure(0, weight=1)
        instructions_frame.grid_columnconfigure(0, weight=1)

        instrText = Text(instructions_frame, height=30, width=120)
        instrText.pack()
        instrText.insert(END, "To Start a customised simulation: \n(If all is left blank and 'start simulation' is\n"
                              "pressed, the default world and values will be used.)\n\n"
                      "1. Insert a matrix on the 'Insert world matrix' box or choose it from a text file\n"
                      "   for the type of world to simulate.\n"
                      "   0 -- Empty space[WHITE]\n"
                      "   4 -- Impassable space[BLACK]\n"
                      "   1 -- Agent 1 [BLUE], agent 2's objective\n"
                      "   5 -- Objective for agent 1[GREEN]\n"
                      "   2 -- Agent 2 [RED]\n"
                      "   6 -- pit [GREY](negative rewards for both agents 1 and 2)\n"
                      "   7 -- secondary objective for agent 1 [YELLOW](does not end round)\n\n"
                      "  Example matrix:\n"
                      "   100044\n"
                      "   006600\n"
                      "   020005\n"
                      "   040400\n\n"
                      "2. Set the algorithm to be used by each agent in the 'choose algorithm' tab. The default\n"
                      "   is temporal difference q-learning.\n"
                      "   -- To choose one, select it from the list of available algorithms and set it to agent 1 and/or 2\n"
                      "   -- To change the default values for variables, insert the value/s to change in the corresponding\n"
                      "      text boxes and choose 'set these values'\n"
                      "   -- Default values for alphas: 0.9, gammas: 0.1, epsilons: 20\n\n"
                      "3. Insert the number of iterations to perform (default = 100000000)\n\n"
                      "4. Set the speed of simulation by inserting a number 1 or greater the 'speed of simulation' entry\n"
                      "   (default speed = 20)\n\n"
                      "5. Toggle the display on and off by selecting 'settings' and the 'simulation on' and \n"
                      "   'simulation off' buttons from the ‘settings’ menu before starting the simulation or while on pause.\n\n"
                      "6. Set the value for the graph display in the 'settings' menu where the number of wins per x\n"
                      "   iterations can be changed.\n\n"
                      "7. Press the 'start simulation' button to begin. It can be paused instantly by pressing the\n"
                      "   'pause now' or 'close' buttons. To wait until a round finishes to stop it, press 'pause'.\n\n"
                      "8. One can view the progress of both agents by clicking on the 'view progress graph' button."
                      "   The progress graph for agent 1 will only be shown if it is the only agent present in the"
                      "   simulation. Used for testing different variable values and learning algorithms.\n\n"
                      "9. To print the current policy of the agents, choose 'view policies'.\n\n"
                      "10.To re-start the simulation and edit the world Matrix, choose 'restart'. If you cancel the\n"
                      "   choosing of a matrix from a text file and get an error when starting the simulation, make sure\n"
                      "   to press 'restart' and try again.\n\n"
                      "11.To learn how to insert new algorithms, refer to the 'Readme' file.")
        instrText.config(state=DISABLED)

        scrollb = tk.Scrollbar(instructions_frame, command=instrText.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        instrText['yscrollcommand'] = scrollb.set

    # ------------------------------------------------------------------------------------------------------
    # Graph to show the number of wins for each agent every certain unit of steps
    # ------------------------------------------------------------------------------------------------------
    def viewGraph(self):

        graph = plt.figure()
        graph.canvas.set_window_title('Progress Graph')

        plt.figure(1)  # the first figure
        plt.subplot(211)  # the first subplot in the first figure
        plt.plot(self.agent1Progress, label='Ag1')
        plt.plot(self.agent2Progress, label='Ag2')
        plt.title("Progress graph for both agents")
        plt.ylabel('Number of wins every ' + str(self.graphSettings) + ' iterations')
        plt.xlabel('Number of iterations (1 unit = ' + str(self.graphSettings) + ' iterations)')

        graph.show()

    # ------------------------------------------------------------------------------------------------------
    # Graph to show the number of steps taken for agent 1 to reach it's objectve
    # ------------------------------------------------------------------------------------------------------
    def viewGraphAgent1(self):
        graph = plt.figure()
        graph.canvas.set_window_title('Progress Graph Agent 1')

        plt.figure(1)  # the first figure
        plt.subplot(211)  # the first subplot in the first figure
        plt.plot(self.agent1StepCount, label='Ag1')
        plt.title("Progress graph for agent 1")
        plt.ylabel('Number of steps before reaching goal')
        plt.xlabel('Round number')

        graph.show()

# ------------------------------------------------------------------------------------------------------
#  Initialisation
# ------------------------------------------------------------------------------------------------------

class Control():
    import Controller

    def __init__(self):
        n = 0;

if __name__ == '__main__':

    sim = Interface();
    sim.startup()
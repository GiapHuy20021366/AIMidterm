# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from pickle import STOP
from game import Agent
from game import Directions
from searchProblems import PositionSearchProblem

import util
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'): #ClosestDotAgent #MyAgent
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        startPosition = state.getPacmanPosition(self.index)
        self.food = state.getFood()
        self.walls = state.getWalls()
        problem = AnyFoodSearchProblem(state, self.index)

        numPacmen = state.getNumPacmanAgents()
        index = self.index    
        # print("agent index ", index, "/", numPacmen, ": ")
        # print("startPOS: ", startPosition)  

        global targets, numFood
        if len(targets) == 0: targets = [(-1,-1) for i in range(0, numPacmen)]
        if numFood is None: numFood = state.getNumFood()
        # print(targets)
        # print(paths)

        # for agentIndex, target in enumerate(targets):
        #     if agentIndex != index and target != (-1,-1):
        #         self.walls[target[0]][target[1]] = True
        #         self.food[target[0]][target[1]] = False
        # problem.food = self.food
        # problem.walls = self.walls

        if numFood == 0: # no un-targeted food
            if len(self.path) == 0: return Directions.STOP

        if targets[index] == (-1,-1) \
            or self.food[targets[index][0]][targets[index][1]] == False \
            or len(self.path) < 1:          
            if numFood > 0:
                targets[index], self.path = search.breadthFirstSearch(problem)
                numFood -= 1
                # print(targets[index])
                # print(numFood)
            
                # for i in range(0, numPacmen):
                #     # print('/t', i, "/", numPacmen)
                #     if i != index: 
                #         # print("/t", i)
                #         state.getPacmanState.getFood[targets[index][0]][targets[index][1]] = False      
                #         state.getPacmanState.getWalls[targets[index][0]][targets[index][1]] = True     
    
        # print(targets)
        action = self.path[0]
        del self.path[0]
        return action
        # raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        global targets, numFood # numFood: # of food not targeted
        targets = [] # food is being targeted by Pac-men/All-agents
        numFood = None

        self.path = []
        self.food = []
        self.walls = []

        # raise NotImplementedError()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"        
        # return search.aStarSearch(problem)[1]
        return search.breadthFirstSearch(problem)[1]  # longest alive
        # return search.uniformCostSearch(problem)
        # return search.depthFirstSearch(problem)   # fastest death

        util.raiseNotDefined()

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"

        global targets

        if self.food[x][y] and (x,y) not in targets:
            # targets[self.agentIndex] = x,y
            # print(targets)
            return True

        return False
        util.raiseNotDefined()


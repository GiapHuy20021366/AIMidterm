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
# def createAgents(num_pacmen, agent='ClosestDotAgent'):
#     return [eval(agent)(index=i) for i in range(num_pacmen)]
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

paths = [None for i in range(10)]
targets = [None for i in range(10)]
force_stop = [False for i in range(10)]
class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        global targets
        global paths
        global force_stop
        startPosition = state.getPacmanPosition(self.index)
        food = state.getFood()
        walls = state.getWalls()  
        problem = AnyFoodSearchProblem(state, self.index)

        if force_stop[self.index]:
            return Directions.STOP

        target = targets[self.index]
        if target is not None and not food[target[0]][target[1]]: 
            targets[self.index] = None
            paths[self.index] = None
            # targets = [None for i in range(10)]
            # paths = [None for i in range(10)]
        
        for target in targets:
            if target is not None:
                food[target[0]][target[1]] = False
        problem.food = food
        
        # if targets[self.index] is None:
        #     for agentIndex,targetIndex in enumerate(targets):
        #         if targetIndex is not None:
        #             mht = util.manhattanDistance(targetIndex, startPosition)
        #             if mht <= len(paths[agentIndex]) and mht < 2:
        #                 # Let many pacman eat a target together
        #                 pos_problem = PositionSearchProblem(state, agentIndex=self.index, goal=targetIndex, start = startPosition)
        #                 path, target = search.breadthFirstSearch(pos_problem)
        #                 targets[self.index] = target
        #                 paths[self.index] = path
        #                 break
                    
        if targets[self.index] is None:
            while len(food.asList()) > 0:
                path, target = search.breadthFirstSearch(problem)
                if target in targets:
                    food[target[0]][target[1]] = False
                    problem.food = food
                else:
                    targets[self.index] = target
                    paths[self.index] = path
                    break
        
        # When number of dot < number of agent: Devide food again
        if targets[self.index] is None:
            for agentIndex,targetIndex in enumerate(targets):
                if targetIndex is not None:
                    mht = util.manhattanDistance(targetIndex, startPosition)
                    if mht < len(paths[agentIndex]) and mht < 5:
                        # Let many pacman eat a target together
                        pos_problem = PositionSearchProblem(state, agentIndex=self.index, goal=targetIndex, start = startPosition)
                        path, target = search.breadthFirstSearch(pos_problem)
                        if len(path) < len(paths[agentIndex]):
                            targets[self.index] = target
                            paths[self.index] = path
                            targets[agentIndex] = None
                            force_stop[agentIndex] = True
                            break
                        break
                        
                    
                   
        if targets[self.index] is not None:
            action = paths[self.index][0]
            del paths[self.index][0]
            return action
        
        if targets[self.index] is None:
            return Directions.STOP
    
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
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
        # print(self.index)
        return search.aStarSearch(problem)
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
        
        self.agentIndex = agentIndex
        self.gameState = gameState

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"   
        return self.food[x][y]
        util.raiseNotDefined()


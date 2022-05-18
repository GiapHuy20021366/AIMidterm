# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print(newPos)
        # print(newFood.asList())
        # print(newGhostStates[0], '|||',  newGhostStates[1])
        # print(newGhostStates[0].getPosition())
        # print(newScaredTimes)
        newFood = newFood.asList() #List position of foods
        ghostPos = [G.getPosition() for G in newGhostStates] #List position of ghosts
        nearest_ghost = min(ghostPos, key = lambda ghost_pos: util.manhattanDistance(ghost_pos, newPos))
        nearest_ghost_mhtd = util.manhattanDistance(nearest_ghost, newPos)
        scared = min(newScaredTimes) > 0  #ScaredTimes[...] for every ghost, maybe time
        if not scared and (newPos in ghostPos): return -1.0
        if scared:
            if nearest_ghost_mhtd < min(newScaredTimes):
                return 1 / nearest_ghost_mhtd + 1 
        if newPos in currentGameState.getFood().asList():  return 1
        
        nearest_food = min(newFood, key = lambda food_pos: util.manhattanDistance(food_pos, newPos)) 
        nearest_food_mhtd = util.manhattanDistance(nearest_food, newPos)
        
        return 1 / nearest_food_mhtd - 1.5 / nearest_ghost_mhtd 
        
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState, getBestAction = False):
            # stop neu win or lose or depth is max
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1
            
            # pacman -> find max value
            if agentIndex == 0:
                scores = [minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions]
                max_score = max(scores)
                return actions[scores.index(max_score)] if getBestAction else max_score 

            # ghost -> find min value
            if gameState.getNumAgents() == nextAgent: #last agent
                nextAgent = 0
                depth += 1
            return min(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions)
            
        return minimax(0, 0, gameState, getBestAction=True)
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(agentIndex, depth, gameState, alpha, beta, getBestAction=False):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1
            bestAction = Directions.STOP
            
            # Pacman should find max
            if agentIndex == 0:
                value = float("-inf")
                for action in actions:
                    score = alphabeta(nextAgent, depth, gameState.generateSuccessor(agentIndex, action), alpha, beta)
                    if score > value:
                        bestAction = action
                    value = max(value, score)
                    if (value > beta):
                        return bestAction if getBestAction else value
                    alpha = max(alpha, value)
                return bestAction if getBestAction else value
            
            # Ghost should find min
            if gameState.getNumAgents() == nextAgent: #last agent
                nextAgent = 0
                depth += 1
            value = float("inf")
            for action in actions:
                value = min(value, alphabeta(nextAgent, depth, gameState.generateSuccessor(agentIndex, action), alpha, beta))
                if (value < alpha):
                    return value
                beta = min (beta, value)
            return value
                                    
        alpha = float("-inf")
        beta = float("inf")
        return alphabeta(0, 0, gameState, alpha, beta, getBestAction=True)
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(agentIndex, depth, gameState, getBestAction=False):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            actions = gameState.getLegalActions(agentIndex)
            nextAgent = agentIndex + 1
            
            #Pacman should find max
            if agentIndex == 0:
                scores = [expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions]
                max_score = max(scores)
                return actions[scores.index(max_score)] if getBestAction else max_score 

            # Ghost should find medium
            if gameState.getNumAgents() == nextAgent: #last agent
                nextAgent = 0
                depth += 1
            scores = [expectimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) for action in actions]
            return sum(scores) / len(actions)
                
        return expectimax(0, 0, gameState, getBestAction=True)
     

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    nearestFood = float("inf")
    if len(food.asList())>0:
        for food in food.asList():
            nearestFood = min(nearestFood, manhattanDistance(pos, food))
        foodScore = 10/nearestFood
    else:
        foodScore = 0
    
    nearestGhost = float("inf")
    for ghostState in ghostStates:
        nearestGhost = min(nearestGhost, manhattanDistance(pos,ghostState.configuration.pos))
    if nearestGhost != 0:
        dangerScore = -10/nearestGhost
    else:
        dangerScore = 0
    
    totalScaredTimes = sum(scaredTimes)
    
    return currentGameState.getScore() + foodScore + dangerScore + totalScaredTimes
    

# Abbreviation
better = betterEvaluationFunction

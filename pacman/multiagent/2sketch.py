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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print("legalMoves is:", legalMoves) ##['West', 'Stop', 'East', 'North', 'South']

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        # print("scores:", scores, "chose to move:", legalMoves[chosenIndex])
        # gameState.data.score = bestScore

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        currentPos = currentGameState.getPacmanPosition()
        successorGameState = currentGameState.generatePacmanSuccessor(action)  #Generates the successor state after the specified pacman move
        # print("successorGameState is:", successorGameState)  #那个layout图
        newPos = successorGameState.getPacmanPosition()
        #print("newPosition is:",newPos) # (4, 6)
        newFood = successorGameState.getFood()
        # print("newFood is:", newFood.asList())   #那个grid，可以后续用asList转一下,转成[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
        newGhostStates = successorGameState.getGhostStates()    
        # print("newGhostStates is:",newGhostStates[0].getPosition())   
        #[<game.AgentState object at 0x10aa8bee0>],其实是一个列表，可以取值出来，具体来看，是Ghost: (x,y)=(23.0, 3.0), East
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print("newScaredTimes is:",newScaredTimes)  #[0]

        "*** YOUR CODE HERE ***"
        # current_score = currentGameState.getScore()

        capsule_list = successorGameState.getCapsules()
        # print("capsules:", capsule_list) #[(23, 1)]
        capsule_distance = 0    #距离capsule的总距离
        nearest_capsule = 10000000   #距离最近的capsule的距离
        for i in capsule_list:
            distance = manhattanDistance(i, newPos)
            capsule_distance += distance
            if distance < nearest_capsule:
                nearest_capsule = distance
        scare_time = 0  #怪物的平均惊吓时间
        for i in newScaredTimes:
            scare_time += i
        scare_time = scare_time / len(newScaredTimes)

        ghost_distance = 0  #距离所有怪物的距离和
        nearest_ghost = 100000000   #最近的鬼的距离
        for i in newGhostStates:
            ghost_pos = i.getPosition()
            distance = manhattanDistance(ghost_pos, newPos)
            ghost_distance += distance
            if distance < nearest_ghost:
                nearest_ghost = distance

        food_list = newFood.asList()
        num_food = len(food_list)

        food_distance = 0  #距离所有事物的距离和
        nearest_food = 1000000    #距离最近的食物的距离
        if num_food == 0:   #不写这个的话，nearest food就是10000000，永远不可能吃掉最后一个
            nearest_food = 0
        else:
            farthest_food = 0
            for i in food_list:
                distance = manhattanDistance(i, newPos)
                food_distance += distance
                if distance < nearest_food:
                    nearest_food = distance
                if distance > farthest_food:
                    farthest_food = distance
        
        # print("num_food", num_food, "nearest_food", nearest_food)
        #print("scare_time:", scare_time,"nearest_ghost:",nearest_ghost, "nearest_food:", nearest_food, "num_food:",num_food, "current_score:", current_score)
        import math
        #successorGameState.data.score = scare_time * nearest_capsule + nearest_ghost + 1/nearest_food - num_food - current_score ** 3 + 1000000 * int(not num_food)    #等很久这个
        #successorGameState.data.score = scare_time * nearest_capsule + nearest_ghost - nearest_food - num_food**3 + (current_score - 500) ** 3 + 10000000 * int(not num_food)   #死一次
        
        #successorGameState.data.score = scare_time * nearest_capsule + nearest_ghost - nearest_food - num_food**3 + (current_score - 1000)**3 + 10000000 * int(not num_food)  #死一次
        
        punish_stop = 0     #不让他停下来
        if newPos == currentPos:
            punish_stop = 10

        successor_score = successorGameState.getScore() 
       
        result = 0.5 * nearest_ghost - punish_stop - 0.5 * nearest_food + successor_score
        return result
        # return result

def scoreEvaluationFunction(currentGameState: GameState):
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

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        GhostIndex = [i for i in range(1, gameState.getNumAgents())]
        ## 对当前幽灵的下一步动作进行遍历，要递归调用以计算其他幽灵的行动

        def term(state, d):
            return state.isWin() or state.isLose() or d == self.depth

        def min_value(state, d, ghost):  

            if term(state, d):
                return self.evaluationFunction(state)

            v = 10000000000000000
            for action in state.getLegalActions(ghost):
            #min_value函数会反复调用获得幽灵的下一步操作
                if ghost == GhostIndex[-1]:
                    v = min(v, max_value(state.generateSuccessor(ghost, action), d + 1))
#如果当前幽灵已经是最后一个，那么应该计算Pacman的行为，调用max_value函数
                else:
                    v = min(v, min_value(state.generateSuccessor(ghost, action), d, ghost + 1))
            return v

        def max_value(state, d):  

            if term(state, d):
                return self.evaluationFunction(state)

            v = -10000000000000000
            for action in state.getLegalActions(0):
            #获得Pacman下一步所有的合法动作
                v = max(v, min_value(state.generateSuccessor(0, action), d, 1))
            return v

        res = [(action, min_value(gameState.generateSuccessor(0, action), 0, 1)) for action in
               gameState.getLegalActions(0)]
        res.sort(key=lambda k: k[1])
       

        return res[-1][0]

        util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

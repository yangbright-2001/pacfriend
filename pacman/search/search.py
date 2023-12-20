# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    fringe = util.Stack()
    fringe.push([problem.getStartState(),[problem.getStartState()]])   #返回的是一个坐标值（5，5）

    closed_set = set()

    while True:

        if fringe.isEmpty():
            return
        
        element = fringe.pop()  #node也是一个坐标值
        node = element[0]
        list_path = element[1]

        if problem.isGoalState(node):   
            break

        elif node not in closed_set:
            closed_set.add(node)   
            successors = problem.getSuccessors(node)   

            # print("successors is: ", successors)       
            
            for i in range(len(successors)):
                # print("successor for node ", node, "is ", successors[i][0])
                fringe.push([successors[i][0], list_path + [successors[i][1]]])
    

    path = list_path[1:]    #要返回每个successors tuple的第二个元素

    return path
    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState()) #(5,5)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))   
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))  
    # #((4, 13), 'North', 1)
    
    fringe = util.Queue()
    fringe.push([problem.getStartState(),[problem.getStartState()]])   #返回的是一个坐标值（5，5）

    closed_set = set()

    while True:
        if fringe.isEmpty():
            return
        element = fringe.pop()  #node也是一个坐标值
        node = element[0]
        list_path = element[1]
        # print("state is ",node)
        # print("type of state is:",type(node))
        
        # print(closed_set)
        if problem.isGoalState(node):   
            # print("fuck3")
            break
        elif node not in closed_set:
            
            closed_set.add(node)   
            successors = problem.getSuccessors(node)   

            # print("successors is: ", successors)       
            
            for i in range(len(successors)):
                # print("successor for node ", node, "is ", successors[i][0])
                fringe.push([successors[i][0], list_path + [successors[i][1]]])
    

    path = list_path[1:]    #要返回每个successors tuple的第二个元素

    return path

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState()) #(5,5)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))   
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))  
    # #((4, 13), 'North', 1)

    cost_dict = {}
    fringe = util.PriorityQueue()
    fringe.push([problem.getStartState(),[problem.getStartState()]], 0)   #返回的是一个坐标值（5，5）
    fringe.update([problem.getStartState(),[problem.getStartState()]], 0) 
    cost_dict[problem.getStartState()] = 0

    closed_set = set()

    while True:

        if fringe.isEmpty():
            return
        
        element = fringe.pop()  #node也是一个坐标值
        node = element[0]
        list_path = element[1]

        if problem.isGoalState(node):   
            break

        elif node not in closed_set:
            closed_set.add(node)   
            successors = problem.getSuccessors(node)   
            # print("getsuccesor to node:",node, "its successors are", successors)

            # print("successors is: ", successors)       
            
            for i in range(len(successors)):
                # print("successor for node ", node, "is ", successors[i][0])
                cost_dict[successors[i][0]] = cost_dict[node] + successors[i][2]    #算总账，cumulative cost
                fringe.push([successors[i][0], list_path + [successors[i][1]]],cost_dict[successors[i][0]] )
                fringe.update([successors[i][0], list_path + [successors[i][1]]],cost_dict[successors[i][0]])
    

    path = list_path[1:]    #要返回每个successors tuple的第二个元素

    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    # print("Start:", problem.getStartState()) #(5,5)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))   
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))  
    # #((4, 13), 'North', 1)

    cost_dict = {}
    astar_dict = {}
    # print("heuristic function is ", heuristic)
    # print("DEBUG: ",problem.getStartState())
    # print("heuristic at ", problem.getStartState(), "is:",heuristic(problem.getStartState(),problem))
    start_node = problem.getStartState()
    cost_dict[start_node] = 0
    astar_dict[start_node] = heuristic(start_node,problem)
    # print("DEBUG:",cost_dict)
    fringe = util.PriorityQueue()
    fringe.push([start_node,[start_node]], astar_dict[start_node])   #返回的是一个坐标值（5，5）
    fringe.update([start_node,[start_node]], astar_dict[start_node]) 

    closed_set = set()

    while True:

        if fringe.isEmpty():
            return
        
        element = fringe.pop()  #node也是一个坐标值
        node = element[0]
        list_path = element[1]

        if problem.isGoalState(node):   
            break

        elif node not in closed_set:
            closed_set.add(node)   
            successors = problem.getSuccessors(node)   
            # print("succesor to node:",node, "are", successors)
            
            for i in range(len(successors)):
                # print("heuristic at ", successors[i][0], "is:", heuristic(successors[i][0], problem))
                # print("successor for node ", node, "is ", successors[i][0])
                successor_node = successors[i][0]
                new_cost = cost_dict[node] + successors[i][2]
                new_astar = new_cost + heuristic(successor_node,problem)
                # print("successor is:",successors[i][0])
                if successor_node not in cost_dict and successor_node not in astar_dict:
                    cost_dict[successor_node] = new_cost  #算总账，cumulative cost
                    astar_dict[successor_node] = new_astar
                elif successor_node in cost_dict and successor_node in astar_dict and new_cost < cost_dict[successor_node] and new_astar < astar_dict[successor_node]:
                    cost_dict[successor_node] = new_cost
                    astar_dict[successor_node] = new_astar
                fringe.push([successor_node, list_path + [successors[i][1]]],astar_dict[successor_node])
                fringe.update([successor_node, list_path + [successors[i][1]]],astar_dict[successor_node])
    
    # print(cost_dict)
    # print(astar_dict)
    
    path = list_path[1:]    #要返回每个successors tuple的第二个元素

    return path

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

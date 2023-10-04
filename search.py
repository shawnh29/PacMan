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

def depthFirstSearch(problem):
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
    print("\n")
    print(type(problem))
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    print("\n")

    # problem.getStartState() gets called only once
    visited = {}  # dictionary that stores the visited nodes and how (what direction) we took to get there
    stack = util.Stack()
    moves = [] # holds the list of moves that leads PacMan to goal state (ex. "West", "South")
    path = {} # 

    stack.push((problem.getStartState(), "", 0))
    visited[problem.getStartState()] = ""
    if problem.isGoalState(problem.getStartState()):
        return 
    
    while stack:
        cur = stack.pop()
        visited[cur[0]] = cur[1] # ex. (5,4) : West
        if problem.isGoalState(cur[0]):
            last = cur[0]
            break
        # if a successor has not been visited, add it to the stack and the path, along with the current node
        for adjacent in problem.getSuccessors(cur[0]):
            if adjacent[0] not in visited.keys():
                stack.push(adjacent)
                path[adjacent[0]] = cur[0]  # ex. (4,5) : (4,4)

    # last is the node that is the goal state, so we are back-tracking
    while last in path.keys():
        temp = path[last]
        moves.insert(0, visited[last]) # 'visited[last]' is the action required to get to the 'last' node (i.e. "West", "South", etc.)
        last = temp
    return moves
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    visited = {}  # dictionary that stores the visited nodes and how (what direction) we took to get there
    queue = util.Queue()
    moves = [] # holds the list of moves that leads PacMan to goal state (ex. "West", "South")
    path = {} 

    queue.push((problem.getStartState(), "", 0))
    visited[problem.getStartState()] = ""
    if problem.isGoalState(problem.getStartState()):
        return 
    
    while queue:
        cur = queue.pop()
        visited[cur[0]] = cur[1] # ex. (5,4) : West
        if problem.isGoalState(cur[0]):
            last = cur[0]
            break
        # if a successor has not been visited, add it to the queue and the path, along with the current node
        for adjacent in problem.getSuccessors(cur[0]):
            if adjacent[0] not in path.keys() and adjacent[0] not in visited.keys():
                queue.push(adjacent)
                path[adjacent[0]] = cur[0]  # ex. (4,5) : (4,4)

    # last is the node that is the goal state, so we are back-tracking
    while last in path.keys():
        temp = path[last]
        moves.insert(0, visited[last]) # 'visited[last]' is the action required to get to the 'last' node (i.e. "West", "South", etc.)
        last = temp
    return moves
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = {}  # dictionary that stores the visited nodes and how (what direction) we took to get there
    pq = util.PriorityQueue()
    moves = [] # holds the list of moves that leads PacMan to goal state (ex. "West", "South")
    path = {} 
    cost_dict = {} # ex. (4,5) : 3 --> (4,5) costs 3 to get to
    # the values in this dict is the TOTAL cost to get to that specific node

    cost_dict[problem.getStartState()] = 0
    pq.push((problem.getStartState(), "", 0), 0)
    visited[problem.getStartState()] = ""
    if problem.isGoalState(problem.getStartState()):
        return
    
    while pq:
        cur = pq.pop()
        visited[cur[0]] = cur[1] # ex. (5,4) : West
        if problem.isGoalState(cur[0]):
            last = cur[0]
            break
        # if a successor has not been visited, add it to the PQ and the path, along with the current node
        for adjacent in problem.getSuccessors(cur[0]):
            if adjacent[0] not in visited.keys():
                priority_val = cur[2] + adjacent[2] # calculate how much it will cost IN TOTAL to get to this adjacent node
                # we push a node onto the pq only if it is not already in the cost_dict OR the new priority value is smaller than the current cost to get to this node
                if adjacent[0] not in cost_dict.keys() or cost_dict[adjacent[0]] > priority_val:
                    pq.push((adjacent[0], adjacent[1], adjacent[2] + cur[2]), priority_val)
                    path[adjacent[0]] = cur[0]  # ex. (4,5) : (4,4)
                    cost_dict[adjacent[0]] = priority_val

    # last is the node that is the goal state, so we are back-tracking
    while last in path.keys():
        temp = path[last]
        moves.insert(0, visited[last]) # 'visited[last]' is the action required to get to the 'last' node (i.e. "West", "South", etc.)
        last = temp
    return moves
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = {}  # dictionary that stores the visited nodes and how (what direction) we took to get there
    pq = util.PriorityQueue()
    moves = [] # holds the list of moves that leads PacMan to goal state (ex. "West", "South")
    path = {} 
    cost_dict_w_H = {} # ex. (4,5) : 3 --> (4,5) costs 3 to get to
    # the values in this dict is the TOTAL cost to get to that specific node

    cost_dict_w_H[problem.getStartState()] = 0
    pq.push((problem.getStartState(), "", 0), 0)
    visited[problem.getStartState()] = ""
    if problem.isGoalState(problem.getStartState()):
        return
    
    while pq:
        cur = pq.pop()
        visited[cur[0]] = cur[1] # ex. (5,4) : West
        if problem.isGoalState(cur[0]):
            last = cur[0]
            break
        # if a successor has not been visited, add it to the PQ and the path, along with the current node
        for adjacent in problem.getSuccessors(cur[0]):
            if adjacent[0] not in visited.keys():
                priority_val = cur[2] + adjacent[2] + heuristic(adjacent[0], problem)# calculate how much it will cost IN TOTAL to get to this adjacent node
                # we push a node onto the pq only if it is not already in the cost_dict OR the new priority value is smaller than the current cost to get to this node
                if adjacent[0] not in cost_dict_w_H.keys() or cost_dict_w_H[adjacent[0]] > priority_val:
                    pq.push((adjacent[0], adjacent[1], adjacent[2] + cur[2]), priority_val)
                    path[adjacent[0]] = cur[0]  # ex. (4,5) : (4,4)
                    cost_dict_w_H[adjacent[0]] = priority_val

    # last is the node that is the goal state, so we are back-tracking
    while last in path.keys():
        temp = path[last]
        moves.insert(0, visited[last]) # 'visited[last]' is the action required to get to the 'last' node (i.e. "West", "South", etc.)
        last = temp
    return moves
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

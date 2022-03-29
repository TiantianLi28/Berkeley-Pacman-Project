# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

'''THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING CODE
WRITTEN BY OTHER STUDENTS.
Tiantian Li '''
"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = path_cost
        
    
    def get_path(self):
        path=[]
        curNode=self
        while curNode.parent is not None:
            #print("curNode:", curNode.get_state())
            path.insert(0,curNode.get_action())
            curNode=curNode.parent
        return path

    def get_state(self):
        return self.state

    def get_action(self):
        return self.action
    

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    nodes=util.Stack()
    start=Node(problem.getStartState(), None, None, 0)
    nodes.push(start)
    seen={}
    while not nodes.isEmpty():
        cur=nodes.pop()
        if problem.isGoalState(cur.get_state()):
            return cur.get_path()
        seen[cur.get_state()]=1
        successors=problem.getSuccessors(cur.get_state())
        for suc in successors:
            if seen.get(suc[0],0)==0:
                #print(suc[0], cur.get_state())
                nodes.push(Node(suc[0], cur, suc[1], 0))
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    nodes=util.Queue()
    start=Node(problem.getStartState(), None, None, 0)
    nodes.push(start)
    seen={}
    seen[start.get_state]=1
    while not nodes.isEmpty():
        cur=nodes.pop()
        seen[cur.get_state()]=1
        if problem.isGoalState(cur.get_state()):
            return cur.get_path()
        successors=problem.getSuccessors(cur.get_state())
        for suc in successors:
            if seen.get(suc[0],0)==0:
                nodes.push(Node(suc[0], cur, suc[1], 0))
                seen[suc[0]]=1
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    nodes=util.PriorityQueue()
    start=Node(problem.getStartState(), None, None, 0)
    nodes.push(start,0)
    seen={}
    while not nodes.isEmpty():
        cur=nodes.pop()
        if seen.get(cur.get_state(),0)==0:
            seen[cur.get_state()]=1
            if problem.isGoalState(cur.get_state()):
                return cur.get_path()
            successors=problem.getSuccessors(cur.get_state())
            for suc in successors:
                if seen.get(suc[0],0)==0:
                    nodes.push(Node(suc[0], cur, suc[1], cur.cost+suc[2]), cur.cost+suc[2])
                    
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    nodes=util.PriorityQueue()
    start=Node(problem.getStartState(), None, None, 0)
    nodes.push(start,0)
    seen={}
    while not nodes.isEmpty():
        cur=nodes.pop()
        if seen.get(cur.get_state(),0)==0:
            seen[cur.get_state()]=1
            if problem.isGoalState(cur.get_state()):
                return cur.get_path()
            successors=problem.getSuccessors(cur.get_state())
            for suc in successors:
                if seen.get(suc[0],0)==0:
                    nodes.push(Node(suc[0], cur, suc[1], cur.cost+suc[2]), heuristic(suc[0], problem)+cur.cost+suc[2])
                    #seen[suc[0]]=1
        #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

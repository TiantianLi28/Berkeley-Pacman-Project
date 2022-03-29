# multiAgents.py
# --------------
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
#
# Modified by Eugene Agichtein for CS325 Sp 2014 (eugene@mathcs.emory.edu)
#
'''THIS CODE IS MY OWN WORK, IT WAS WRITTEN WITHOUT CONSULTING CODE
WRITTEN BY OTHER STUDENTS.
Tiantian Li '''

from audioop import minmax
from locale import currency

from util import manhattanDistance
from game import Directions
import random, util, search

from game import Agent
from game import Actions



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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        Note that the successor game state includes updates such as available food,
        e.g., would *not* include the food eaten at the successor state's pacman position
        as that food is no longer remaining.
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currentFood = currentGameState.getFood() #food available from current state
        newFood = successorGameState.getFood() #food available from successor state (excludes food@successor) 
        currentCapsules=currentGameState.getCapsules() #power pellets/capsules available from current state
        newCapsules=successorGameState.getCapsules() #capsules available from successor (excludes capsules@successor)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #if about to lose, return negative infinity
        if currentGameState.isLose(): 
          return -float("inf")
        #if about to win, return positive infinity
        elif currentGameState.isWin():
          return float("inf")
        #distance to nearest ghost
        ghost_dis=999
        #distance to nearest scared ghost
        scared_ghost=99999
        #list of food
        newFoodl=newFood.asList()
        currentScore = scoreEvaluationFunction(currentGameState)
        newScore = successorGameState.getScore()
        diff=newScore-currentScore
        #find distance to nearest ghost
        for states in newGhostStates:
          dis=manhattanDistance(states.getPosition(), newPos)
          if states.scaredTimer:
            if dis<scared_ghost:
              scared_ghost=dis
          else:
            if dis<ghost_dis:
              ghost_dis=dis
        #find distance to nearest food
        food_dis=len(newFoodl)*999999
        for food in newFoodl:
          dis=manhattanDistance(food, newPos)
          if dis<food_dis:
            food_dis=dis
        #find distance to nearest capsule
        cap_dis=len(newCapsules)*99999
        for states in newCapsules:
          dis=manhattanDistance(states, newPos)
          if dis<cap_dis:
            cap_dis=dis
        
        if(ghost_dis==0):
          return -float("inf")
        if(scared_ghost==99999):
          scared_ghost=0
        #return a linear combination of the above features
        score = (-2*food_dis)+2*ghost_dis-10*newFood.count()-4*len(newCapsules)-4*scared_ghost+5*diff
        return score
        

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
        """
        "*** YOUR CODE HERE ***"
      
        def minimax_decision(state):
            susState=[]
            best_action=None
            #v holds the largest evaluation value
            v=-float("inf")
            #get all state reachable
            for action in state.getLegalActions(0):
                susState.append((state.generateSuccessor(0, action), action))
            #call minValue on all successor states
            for sstate in susState:
                substate=sstate[0]
                evaluation=minValue(substate, 1, 0)
                if evaluation>v:
                    v=evaluation
                    best_action=sstate[1]
                    
            return best_action


        #given a state, current agent index, and current depth, return the largest evaluation value
        def maxValue(state, agentIndex, depth):
            
            #check if final state
            if (depth>=self.depth or (len(state.getLegalActions(0)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=-float("inf")
          
            #generate successor states
            susState=[]
            for action in state.getLegalActions(agentIndex):
                susState.append(state.generateSuccessor(agentIndex, action))
            #find max v
            for susState in susState:
                v=max(v, minValue(susState, 1, depth))
            return v
            
        
        def minValue(state, agentIndex, depth):
            #check if final state
            if ((len(state.getLegalActions(agentIndex)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=float("inf")

            #generate successor states
            susState=[]
            for action in state.getLegalActions(agentIndex):
                susState.append(state.generateSuccessor(agentIndex, action))

            for substate in susState:
                #if agent is min 
                if agentIndex<(substate.getNumAgents()-1):
                    v=min(v,minValue(substate, agentIndex+1, depth))
                else:
                    v=min(v,maxValue(substate, 0, depth+1))
            return v

        return minimax_decision(gameState)
      

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimax_decision(state):
            #max's best option on path to root
            alpha=-float("inf")
            #min's best option on path to root
            beta=float("inf")
           
            susState=[]
            best_action=None

            for action in state.getLegalActions(0):
                susState.append((state.generateSuccessor(0, action), action))
            
            for sstate in susState:
                substate=sstate[0]
                evaluation=minValue(substate, 1, 0, alpha, beta)
                if evaluation>alpha:
                    alpha=evaluation
                    best_action=sstate[1]
                    
            return best_action



        def maxValue(state, agentIndex, depth, alpha, beta):
            #check if final state
            if (depth>=self.depth or (len(state.getLegalActions(0)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=-float("inf")
            #generate successor states
            susState=[]
            for action in state.getLegalActions(agentIndex):
                susState=state.generateSuccessor(agentIndex, action)
                v=max(v, minValue(susState, 1, depth, alpha, beta))
                if v> beta:
                    return v
                alpha= max(alpha, v)
                
            return v
            

        def minValue(state, agentIndex, depth, alpha, beta):
            #check if final state
            if ((len(state.getLegalActions(agentIndex)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=float("inf")

            #generate successor states
            
            for action in state.getLegalActions(agentIndex):
                substate=(state.generateSuccessor(agentIndex, action))
                #if agent is min 
                if agentIndex<(substate.getNumAgents()-1):
                    v=min(v,minValue(substate, agentIndex+1, depth, alpha, beta))
                else:
                    v=min(v,maxValue(substate, 0, depth+1, alpha, beta))
                if v< alpha:
                    
                    return v
                beta=min(beta, v)
            return v

        return minimax_decision(gameState)
        util.raiseNotDefined()

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
        def minimax_decision(state):
            #max's best option on path to root
            
            #min's best option on path to root
           
            alpha=-float("inf")
            susState=[]
            best_action=None

            for action in state.getLegalActions(0):
                
                susState.append((state.generateSuccessor(0, action), action))
            
            for sstate in susState:
              
                substate=sstate[0]
                evaluation=minValue(substate, 1, 0)
                if evaluation>alpha:
                    alpha=evaluation
                    best_action=sstate[1]
                    
            return best_action



        def maxValue(state, agentIndex, depth):
            #check if final state
            if (depth>=self.depth or (len(state.getLegalActions(0)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=-float("inf")
            #generate successor states
            susState=[]
            for action in state.getLegalActions(agentIndex):
                susState=state.generateSuccessor(agentIndex, action)
                v=max(v, minValue(susState, 1, depth))
            return v
            

        def minValue(state, agentIndex, depth):
            #check if final state
            if ((len(state.getLegalActions(agentIndex)) == 0)):
                return self.evaluationFunction(state)

            #initialize v
            v=0

            #generate successor states
            susState=[]
            for action in state.getLegalActions(agentIndex):
                susState.append(state.generateSuccessor(agentIndex, action))

            for substate in susState:
                #if agent is min 
                if agentIndex<(substate.getNumAgents()-1):
                    v+=minValue(substate, agentIndex+1, depth)
                else:
                    v+=maxValue(substate, 0, depth+1)
            
            return v/len(state.getLegalActions(agentIndex)) 

        return minimax_decision(gameState)
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: calculated the number of food left, the number of capsules left, distance to nearest scared ghost and 
      distance to nearest enemy ghost, and distance to closest food. Then output a linear combination of the attributes. 
    """

    "*** YOUR CODE HERE ***"
    
    if currentGameState.isWin():
        
        return float("inf")

    currentPos=currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood().asList()
    currentCapsule= currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scared_ghosts_timer = [ghost_state.scaredTimer for ghost_state in ghostStates]
    
    
    numFood=len(currentFood)
    numCap=len(currentCapsule)
    scaredGhost=[]
    enemyGhost=[]
    #distinguish the scared and enemy ghosts
    for g in ghostStates:
        if g.scaredTimer == 0:
            enemyGhost.append(g)
        else:
            scaredGhost.append(g)
    
    #find closest food:
    closestFood=9999
    for food in currentFood:
        dis=manhattanDistance(currentPos, food)
        if dis<closestFood:
            closestFood=dis
    
    #find closest scared ghost:
    closestScaredGhost=9999
    for sg in scaredGhost:
        dis=manhattanDistance(currentPos, sg.getPosition())
        if dis< closestScaredGhost:
            closestScaredGhost=dis
    
    #find closest enemy ghost:
    closestEnemyGhost=9999
    for eg in enemyGhost:
        dis=manhattanDistance(currentPos, eg.getPosition())
        if dis< closestEnemyGhost:
            closestEnemyGhost=dis
    
    if closestFood==9999:
        closestFood=0
    
    score=1.0/closestFood-(1.0/(closestEnemyGhost+0.1))-10.0*closestScaredGhost-20.0*numCap-2.0*numFood+2*currentGameState.getScore()

        

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


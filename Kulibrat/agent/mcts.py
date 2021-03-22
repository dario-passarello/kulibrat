import numpy as np
from collections import defaultdict

class MCTS():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
    
    def untried_actions(self):
    
        self._untried_actions = self.state.check_legal_actions()
        return self._untried_actions
    
    def q(self): # win - losses 
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses
    
    def n(self): # number of times the node was visited
        return self._number_of_visits
    
    def expand(self):
    	
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MCTS(next_state, parent=self, parent_action=action)
    
        self.children.append(child_node)
        return child_node 
    
    
    def is_terminal_node(self):
        return self.state.check_game_over()
    
    def rollout(self):
        current_rollout_state = self.state
        
        while not current_rollout_state.check_game_over():
            
            possible_moves = current_rollout_state.check_legal_actions()
            
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result()
    
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)
            
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def rollout_policy(self, possible_moves):
        
        return possible_moves[np.random.randint(len(possible_moves))]
    
    def _tree_policy(self):
    
        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.simulation()
        return current_node
    
    def simulation(self):
        simulation_no = 100
        for i in range(simulation_no):
    		
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
    	
        return self.best_child(c_param=0.)

    def check_legal_actions(self): 
   # def get_possible_actions(self):
        '''
        Get possible actions from DARIO's list
        choose the move function
        '''
        
    def check_game_over(self):
        '''
        Check if the score is 5 for one of the players, 
        or if the game is stuck
        '''
        
    def game_result(self):
        '''
        return 1 for win
        return -1 for losses
        '''
    
    def move(self,action):
        '''
        put the grid state for each moves
    '''
def main():
    root = MCTS(state = 0) # get initial_state from game code
    selected_node = root.simulation()
    return


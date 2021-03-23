from __future__ import annotations
from typing import List, Dict
from Kulibrat.game.game import Action, Kulibrat, Player
from Kulibrat.game.agent import Agent
import numpy as np
import random
import copy
from collections import defaultdict

class MCTSAgent(Agent):
    def __init__(self, game : Kulibrat, player : Player):
        super().__init__(game, player)
        self.tree_root = MCTS(self.player, state = game.copy_state())
        
    def advance_tree_root(self, action : Action) -> MCTS:
        '''
        Moves the tree root to the child indicated from the action
        '''
        child = self.tree_root[action]
        self.tree_root = child
        # Clean parent to activate garbage collection
        self.tree_root.parent = None
        self.tree_root.parent_action = None
        return self.tree_root

    def choose_move(self, actions : List[Action], previous_actions : List[Action] = []) -> Action:
        # Realign tree to the moves made from the opponent

        for action in previous_actions:
            self.advance_tree_root(action)
        # Decide here what move perform and assign it to chosen_action

        chosen_action = self.tree_root.simulation()
        # Align tree on the choice performed
        self.advance_tree_root(chosen_action)
        return chosen_action

class MCTS():
    '''
    Montecarlo Search Tree Node
    
    This tree will lazily generate nodes when they are requested
    Each node stores a game state, the rewards and the number of visits
    '''
    def __init__(self, player : Player, state : Kulibrat, parent=None, parent_action=None):
        self.state = state
        self.player = player
        self.parent = parent
        self.parent_action = parent_action
        self.children : Dict[Action, MCTS] = {}  # key = Action that leads to that state, value = state
        self.number_of_visits : int = 0
        self.results = {Player.BLACK : 0.0, Player.RED : 0.0}
        self.untried_actions = self.state.get_possible_actions()
    

    def __getitem__(self, action : Action) -> MCTS:
        '''
        Returns the child with the specified action.
        Generates the child if it is not yet present
        '''
        if action in self.children:
            return self.children[action]
        else:
            if action in self.state.get_possible_actions():
                e = self.expand(action)
                return e
            else:
                raise ValueError(f'{str(action)} action not permitted in this state')
    

    def q(self): # win - losses 
        wins = self.results[self.player]
        loses = self.results[self.player.opponent()]
        return wins - loses
    
    def expand(self, action : Action) -> MCTS:
        next_state = self.state.copy_state()
        next_state.execute_action(action)
        child_node = MCTS(self.player, next_state, parent=self, parent_action=action)
        self.children[action] = child_node
        return child_node 
    
    
    def is_terminal_node(self) -> bool:
        return self.state.check_game_over()
    
    def rollout(self) -> Player:
        current_rollout_state = self.state.copy_state()
        while not current_rollout_state.check_game_over():
            possible_moves = current_rollout_state.get_possible_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.execute_action(action)
        return current_rollout_state.winner
    
    def backpropagate(self, result : Player) -> None:
        self.number_of_visits += 1
        self.results[result] += 1.
        if self.parent is not None:
            self.parent.backpropagate(result)
            
    
    def is_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0
    
    def rollout_policy(self, possible_actions : List[Action]) -> Action:
        return random.choice(possible_actions)

    def tree_policy(self) -> MCTS:
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                action = current_node.untried_actions.pop()
                return current_node[action]
            else:
                current_node = current_node[current_node.UCBT()]
        return current_node
    
    def simulation(self) -> Action:
        simulation_no = 100
        for _ in range(simulation_no):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.UCBT()

    def UCBT(self) -> Action:
        choices_weights = {action : (child.q() / child.number_of_visits) +  np.sqrt((2 * np.log(self.number_of_visits / child.number_of_visits))) for action, child in self.children.items() if child.number_of_visits > 0}
        return max(choices_weights.keys(), key=lambda v: choices_weights[v])



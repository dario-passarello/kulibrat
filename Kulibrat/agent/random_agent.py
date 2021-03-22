from typing import List
from Kulibrat.game.agent import Agent
import random

from Kulibrat.game.game import Action, Kulibrat, Player

class RandomAgent(Agent):
    def __init__(self, game : Kulibrat, player : Player):
        super().__init__(game, player)
        self.player = player
    
    def choose_move(self, actions : List[Action]) -> Action:
        action = random.choice(actions)
        return action

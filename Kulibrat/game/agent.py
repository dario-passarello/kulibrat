from typing import List
from Kulibrat.game.game import Action, Kulibrat, Player
from abc import abstractmethod

class Agent:
    def __init__(self, game : Kulibrat, player : Player):
        self.game = game # game is available but not access
        self.player = player

    @abstractmethod
    def choose_move(self, actions : List[Action], previous_actions : List[Action] = []) -> Action:
        pass

from typing import List
from Kulibrat.game.game import Action, Kulibrat
from abc import abstractmethod

class Agent:
    def __init__(self, game : Kulibrat):
        self.game = game # game is available but not access

    @abstractmethod
    def choose_move(self, actions : List[Action]) -> Action:
        pass

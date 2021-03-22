
from Kulibrat.game.game import Player, Player, Kulibrat, Action
from Kulibrat.game.agent import Agent
from typing import List
import Kulibrat.game.view as View

class HumanAgent(Agent):
    def __init__(self, game : Kulibrat, player : Player):
        super().__init__(game, player)
    
    def choose_move(self, actions : List[Action], previous_actions : List[Action] = []) -> Action:
        View.draw_grid(self.game)
        opponent = self.player.opponent()
        print(f'SCORE: YOU {self.game.score[self.player]} - {self.game.score[opponent]} {opponent.name}')
        print(f'PLAYER {self.player.name} choose an action:')
        for i, action in enumerate(actions):
            print(f'{i} - {action}')
        while True:
            choice = int(input())
            if 0 <= choice < len(actions):
                return actions[choice]
            print(f'Invalid choice please select a number between 0 and {len(actions) - 1}')










    
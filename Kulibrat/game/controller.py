from Kulibrat.game.agent import Agent
from Kulibrat.game.game import Kulibrat, Player

class Controller:
    def __init__(self, game : Kulibrat, player_black : Agent, player_red : Agent):
        self.game = game
        self.views = {Player.BLACK : player_black, Player.RED : player_red}

    def play(self):
        while self.game.winner == Player.EMPTY:
            action = self.views[self.game.turn].choose_move(self.game.allowed_actions)
            self.game.execute_action(action)
        print(f'Player {self.game.winner.name} Won!')
from Kulibrat.game.agent import Agent
from Kulibrat.game.game import Kulibrat, Player

class Controller:
    def __init__(self, game : Kulibrat, player_black : Agent, player_red : Agent):
        self.game = game
        self.views = {Player.BLACK : player_black, Player.RED : player_red}

    def play(self):
        prev_turn = Player.EMPTY
        prev_actions_list = []
        while self.game.winner == Player.EMPTY:
            curr_turn = self.game.turn
            if curr_turn != prev_turn:
                # Provide the list of the actions made from the other player in the previous turn(s)
                action = self.views[self.game.turn].choose_move(self.game.allowed_actions, prev_actions_list)
                prev_actions_list = [] # Reset the list
            else:
                # The previous player is the same of the current one, no need to communicate the previous moves
                action = self.views[self.game.turn].choose_move(self.game.allowed_actions, [])
            prev_actions_list.append(action) # Add the current action the the previous action list 
            prev_turn = self.game.turn
            self.game.execute_action(action)
                
        print(f'Player {self.game.winner.name} Won!')
from typing import Container
from Kulibrat.game.game import Kulibrat, Player
from Kulibrat.game.controller import Controller
from Kulibrat.agent.human_agent import HumanAgent

if __name__ == "__main__":
    game = Kulibrat()
    player1 = HumanAgent(game, Player.BLACK)
    player2 = HumanAgent(game, Player.RED)
    controller = Controller(game, player1, player2)
    controller.play()

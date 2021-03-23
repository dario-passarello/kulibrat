from Kulibrat.agent.random_agent import RandomAgent
from Kulibrat.agent.mcts import MCTSAgent
from typing import Container
from Kulibrat.game.game import Kulibrat, Player
from Kulibrat.game.controller import Controller
from Kulibrat.agent.human_agent import HumanAgent
from tqdm import tqdm

def setup_agent_vs_random():
    game = Kulibrat(max_score=2)
    player1 = RandomAgent(game, Player.BLACK)
    player2 = MCTSAgent(game, Player.RED)
    controller = Controller(game, player1, player2)
    return controller.play()


def count(n=100):
    results = {Player.BLACK : 0, Player.RED : 0}
    for i in tqdm(range(n)):
        results[setup_agent_vs_random()] += 1
    return results


if __name__ == "__main__":
    print(count(100))

    
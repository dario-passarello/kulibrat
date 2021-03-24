from numpy import result_type
from Kulibrat.agent.random_agent import RandomAgent
from Kulibrat.agent.mcts import MCTSAgent
from typing import Container
from Kulibrat.game.game import Kulibrat, Player
from Kulibrat.game.controller import Controller
from Kulibrat.agent.human_agent import HumanAgent
import sys

def setup_game(black, red, max_score):
    game = Kulibrat(max_score=max_score)
    controller = Controller(game, black, red)
    return controller.play()




def simulate(agent1, agent2, n=100,  max_score = 5):
    first_res = {Player.BLACK : 0, Player.RED : 0}
    second_res = {Player.BLACK : 0, Player.RED : 0}
    for i in range(n // 2):
        print(f'Match {i}')
        game = Kulibrat(max_score=max_score)
        first_res[setup_game(agent1(game, Player.BLACK), agent2(game, Player.RED), max_score)] += 1
    print('Exchanging Colors!')
    for i in range(n // 2):
        print(f'Match {i}')
        game = Kulibrat(max_score=max_score)
        second_res[setup_game(agent2(game, Player.BLACK), agent1(game, Player.RED), max_score)] += 1
    tot_res = {"Agent 1": first_res[Player.BLACK] + second_res[Player.RED], "Agent 2": first_res[Player.RED] + second_res[Player.BLACK]}
    print()
    print(f'Agent 1 () WINS: {tot_res["Agent 1"]} (as black: {first_res[Player.BLACK]}, as red: {second_res[Player.RED]})')
    print(f'Agent 2 () WINS: {tot_res["Agent 2"]} (as black: {first_res[Player.RED]}, as red: {second_res[Player.BLACK]})')
    return first_res, second_res, tot_res


def setup_human(opponent, human_red = False, max_score=5):
    game = Kulibrat(max_score=max_score)
    if human_red:
        human = HumanAgent(game, Player.RED)
        opponent = opponent(game, Player.BLACK)
        controller = Controller(game, opponent, human)
    else:
        human = HumanAgent(game, Player.BLACK)
        opponent = opponent(game, Player.RED)
        controller = Controller(game, human, opponent)
    controller.play()



def menu():
    print('Select type of match')
    print('1 - Human VS Human')
    print('2 - Human VS Random')
    print('3 - Human VS Monte Carlo')
    print('4 - Montecarlo VS Montecarlo')
    print('5 - Montecarlo VS Random')
    print('0 - QUIT')
    choice = int(input('> '))
    if choice == 0:
        sys.exit()
    max_score = int(input('Select max score: '))
    if choice == 1:
        setup_human(opponent=lambda game, color: HumanAgent(game, color), max_score=max_score)
    elif choice == 2:
        human_red = int(input('Press 0 to play as the RED, 1 to play as the BLACK: ')) == 0
        setup_human(opponent=lambda game, color: RandomAgent(game, color), human_red=human_red, max_score=max_score)
    elif choice == 3:
        human_red = int(input('Press 0 to play as the RED, 1 to play as the BLACK: ')) == 0
        setup_human(opponent=lambda game, color: MCTSAgent(game, color), human_red=human_red, max_score=max_score)
    elif choice == 4:
        n_sim = int(input('Number of simulations: '))
        simulate(agent1=lambda game, color: MCTSAgent(game, color, c = 1, max_sim= 15, score_f = lambda x: 1 if x == max_score else 0), agent2=lambda game, color : MCTSAgent(game, color, c = 1, max_sim= 35, score_f = lambda x: 1 if x == max_score else 0), n=n_sim, max_score=max_score)
    elif choice == 5:
        n_sim = int(input('Number of simulations: '))
        simulate(agent1=lambda game, color: MCTSAgent(game, color, c = 1, max_sim= 15, score_f = lambda x: 1 if x == max_score else 0), agent2=lambda game, color : RandomAgent(game, color), n=n_sim, max_score=max_score)
    else:
        a = 1 / 0
if __name__ == "__main__":
    while True:
        menu()

    
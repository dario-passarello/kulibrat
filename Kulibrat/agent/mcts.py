from __future__ import annotations
from typing import List, Dict
from Kulibrat.game.game import Action, Kulibrat, Player
from Kulibrat.game.agent import Agent
import math
import random


class MCTSAgent(Agent):
    """
    An agent that decides his next move building a Monte Carlo Search Tree (MCST)
    """

    def __init__(
        self,
        game: Kulibrat,
        player: Player,
        c=1.0,
        max_sim=15,
        score_f=lambda x: x,
        score_depth=100000,
    ):
        """
        game : Kulibrat
        ---
        The instance of the game in which the agent will take part

        player : Player
        ---
        The color of the player pawns (could be either Player.BLACK or Player.RED)

        c : float
        ---
        The explorative factor, the higher it is the more the UCBT will select an
        unexplored branch instead of a promising one

        max_sim : int
        ---
        The maximum number of game to simulate during the simulation phase
        This parameter could affect the performance of the search if it is too high (> 100)
        15 is the recommended value

        score_f : function
        ---
        A function that takes in input a score (between 0 and game.max_score) and
        returns the reward value used in the backtracking phase

        score_depth : int
        ---
        The maximum increment of the score considered for stopping the simulation.
        (i.e. a game with scores 2-3 and with score_depth 2 will be simulated until
        3 + 2 = 5 points, or when max_score is reached). A lower values increases
        time performances of the search (in game with big max_scores) but if it
        is too low could decrease the quality of the AI
        """
        super().__init__(game, player)
        self.tree_root = MCTS(
            self.player,
            state=game.copy_state(),
            c=c,
            max_sim=max_sim,
            score_f=score_f,
            score_depth=score_depth,
        )
        self.c = c
        self.max_sim = max_sim
        self.score_f = score_f
        self.score_depth = score_depth

    def __str__(self):
        return f"Montecarlo Tree Search Agent c = {self.c}"

    def advance_tree_root(self, action: Action) -> MCTS:
        """
        Moves the tree root to the child indicated from the action
        Removes the parent node from the memory
        """
        child = self.tree_root[action]
        self.tree_root = child
        # Clean parent to activate garbage collection
        self.tree_root.parent = None
        self.tree_root.parent_action = None
        return self.tree_root

    def choose_move(
        self, actions: List[Action], previous_actions: List[Action] = []
    ) -> Action:
        # Realign tree to the moves made from the opponent

        for action in previous_actions:
            self.advance_tree_root(action)
        # Decide here what move perform and assign it to chosen_action

        chosen_action = self.tree_root.simulation()
        # Align tree on the choice performed
        self.advance_tree_root(chosen_action)
        return chosen_action


class MCTS:
    """
    Montecarlo Search Tree Node

    This tree will lazily generate nodes when they are requested
    Each node stores a game state, the rewards and the number of visits
    """

    def __init__(
        self,
        player: Player,
        state: Kulibrat,
        c=1.0,
        max_sim=15,
        score_f=lambda x: x,
        parent=None,
        parent_action=None,
        score_depth=100000,
    ):
        self.state = state
        self.player = player
        self.parent = parent
        self.parent_action = parent_action
        self.children: Dict[
            Action, MCTS
        ] = {}  # key = Action that leads to that state, value = state
        self.number_of_visits: int = 0
        self.results = {Player.BLACK: 0.0, Player.RED: 0.0}
        self.untried_actions = self.state.get_possible_actions()
        random.shuffle(self.untried_actions)
        self.c = c
        self.max_sim = max_sim
        self.score_f = score_f
        self.score_depth = score_depth

    def __getitem__(self, action: Action) -> MCTS:
        """
        Returns the child with the specified action.
        Generates the child if it is not yet present
        """
        if action in self.children:
            return self.children[action]
        else:
            if action in self.state.get_possible_actions():
                e = self.expand(action)
                return e
            else:
                raise ValueError(f"{str(action)} action not permitted in this state")

    def q(self):  # win - losses
        wins = self.results[self.player]
        loses = self.results[self.player.opponent()]
        return wins - loses

    def expand(self, action: Action) -> MCTS:
        next_state = self.state.copy_state()
        next_state.execute_action(action)
        child_node = MCTS(
            self.player,
            next_state,
            self.c,
            self.max_sim,
            self.score_f,
            parent=self,
            parent_action=action,
            score_depth=self.score_depth,
        )
        self.children[action] = child_node
        return child_node

    def is_terminal_node(self, max_score) -> bool:
        if (
            self.state.score[Player.BLACK] >= max_score
            or self.state.score[Player.RED] >= max_score
        ):
            return True
        return self.state.check_game_over()

    def rollout(self) -> Dict[Player, int]:
        current_rollout_state = self.state.copy_state()
        while not current_rollout_state.check_game_over():
            possible_moves = current_rollout_state.get_possible_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.execute_action(action)
        return current_rollout_state.score

    def backpropagate(self, result: Dict[Player, int]) -> None:
        self.number_of_visits += 1
        for player, score in result.items():
            self.results[player] += self.score_f(score)
        if self.parent is not None:
            self.parent.backpropagate(result)

    def is_fully_expanded(self) -> bool:
        return len(self.untried_actions) == 0

    def rollout_policy(self, possible_actions: List[Action]) -> Action:
        return random.choice(possible_actions)

    def tree_policy(self) -> MCTS:
        current_node = self
        max_score = (
            max(self.state.score[Player.BLACK], self.state.score[Player.RED])
            + self.score_depth
        )
        while not current_node.is_terminal_node(max_score):
            if not current_node.is_fully_expanded():
                action = current_node.untried_actions.pop()
                return current_node[action]
            else:
                current_node = current_node[current_node.UCBT()]
        return current_node

    def simulation(self) -> Action:
        for _ in range(self.max_sim):
            v = self.tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.UCBT()

    def UCBT(self) -> Action:
        choices_weights = {
            action: (child.q() / child.number_of_visits)
            + self.c
            * math.sqrt((2 * math.log(self.number_of_visits / child.number_of_visits)))
            for action, child in self.children.items()
            if child.number_of_visits > 0
        }
        return max(choices_weights.keys(), key=lambda v: choices_weights[v])

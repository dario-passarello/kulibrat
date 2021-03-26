from __future__ import annotations
from typing import Dict, List, Tuple, Optional, Union, Iterable
from enum import Enum
import copy

N_ROWS = 4
N_COLS = 3
N_PAWNS = 4

EAST = -1
WEST = 1

WIN_SCORE = 5

class Player(Enum):
    '''
    Represents the pawn color. It could be EMPTY if no pawn is present in a cell
    '''
    EMPTY = -1
    BLACK = 0
    RED = 1

    def row_dir(self):
        '''
        The row direction of the moves of the player
        '''
        if self == Player.BLACK:
            return 1
        if self == Player.RED:
            return -1
        else:
            raise ValueError('Empty player has no row direction')
    
    def check_goal_coord(self, coord) -> bool:
        '''
        Checks if coord is a goal coordinate for the pawn color 
        '''
        if self == Player.BLACK:
            return 0 <= coord.col < N_COLS and coord.row == N_ROWS
        elif self == Player.RED:
            return  0 <= coord.col < N_COLS and coord.row == -1
        else:
            raise ValueError('Empty player has no goal coordinates')
    
    def spawn_row(self):
        '''
        Returns the row in which pawns spawn for that color
        '''
        if self == Player.BLACK:
            return 0
        elif self == Player.RED:
            return N_ROWS - 1
        else:
            raise ValueError('Empty player has no spawn coordinates')
    
    def goal_row(self):
        '''
        Returns the row that pawns of the given color have to reach to score a point
        '''
        if self == Player.BLACK:
            return N_ROWS
        elif self == Player.RED:
            return -1
        else:
            raise ValueError('Empty player has no goal coordinates')
    
    def opponent(self) -> Player:
        '''
        Returns the opponent Player object
        '''
        if self == Player.BLACK:
            return Player.RED
        elif self == Player.RED:
            return Player.BLACK
        else:
            raise ValueError('Empty player has no opponents')
    
    def is_empty(self):
        return self == Player.EMPTY
    
    def is_player(self):
        return self != Player.EMPTY
    
    def get_repr(self):
        if self == Player.BLACK:
            return 'B'
        elif self == Player.RED:
            return 'R'
        else:
            return 'E'


# Color EMPTY means no pawn in the square
# WHen color is EMPTY, the number is unspecified
class Coord:
    def __init__(self, row : int, col : int):
        self.row = row
        self.col = col

    def __add__(self, other):
        if(isinstance(other, Coord)):
            return Coord(self.row + other.row, self.col + other.col)
        elif(isinstance(other, tuple)):
            return Coord(self.row + other[0], self.col + other[1])
        else:
            raise TypeError('Invalid tuple')

    def __eq__(self, other):
        if isinstance(other, Coord):
            return (self.row, self.col) == (other.row, other.col)
        elif isinstance(other, tuple):
            return (self.row, self.col) == other
        else:
            return False
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __repr__(self):
        return f'({self.row}, {self.col})'


class Pawn:
    '''
    Pawn object
    Stores information about color, position and number
    A pawn is an element of the Grid and for this reason could be empty, in that case
    number and position could be None
    '''
    def __init__(self, player : Player, number : Optional[int] = None, position : Optional[Coord] = None):
        self.player = player
        self.number = number
        self.position = position
    
    def keys(self):
        return ['color', 'number', 'position']
    
    def is_empty(self):
        return self.position is None and self.number is None
    
    def is_placed(self):
        return self.position is not None
    
    def copy(self):
        return Pawn(copy.deepcopy(self.player), self.number, Coord(self.position.row, self.position.col) if self.position else None)
    
    def __eq__(self, other):
        return (self.player, self.number) == (other.player, other.number)
    
    def __hash__(self):
        return hash((self.player, self.number))
    
    def __repr__(self):
        return f'{self.player.get_repr()}{str(self.number)}{self.position if self.position is not None else "(-,-)"}'



class Grid:
    '''
    A matrix containing pawns (including empty cells)
    Could be directly accessed supplying a tuple (i.e. grid[2,3]) or a Coord object
    '''
    def __init__(self):
        self.grid = {Coord(i, j): Pawn(Player.EMPTY, None, None) for i in range(-1,N_ROWS + 1) for j in range(-1, N_COLS + 1)}

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False 
        return self.grid == other.grid

    def __getitem__(self, coord : Union[Tuple[int, int], Coord]):
        if isinstance(coord, Coord):
            row, col = coord.row, coord.col
        elif isinstance(coord, tuple):
            row, col = coord
        else:
            raise TypeError('Invalid grid index type')
        return self.grid[Coord(row, col)]

    def __setitem__(self, coord : Union[Tuple[int, int], Coord], new_value : Pawn):
        if isinstance(coord, Coord):
            row, col = coord.row, coord.col
        elif isinstance(coord, tuple):
            row, col = coord
        else:
            raise TypeError('Invalid grid index type')
        self.grid[Coord(row, col)] = new_value
    
    @classmethod
    def grid_from_pawns(cls, pawns : Dict[Player, List[Pawn]]) -> Grid:
        new_grid = Grid()
        for player in pawns.values():
            for pawn in player:
                if pawn.position is not None:
                    new_grid[pawn.position] = pawn
        return new_grid

    def rows(self) -> Iterable[List[Pawn]]:
        for row_n in range(N_ROWS):
            yield [self.grid[Coord(row_n, col)] for col in range(N_COLS)]


class Action:
    '''
    Abstract class representing a potential Action
    Contains information about the player that could performs the action
    and the pawn on which the action is applied
    '''
    def __init__(self, player : Player, pawn : Pawn):
        self.player = player
        self.pawn = pawn

    def __eq__(self, other):
        if type(self) != type(other):
            return False 
        return (self.player, self.pawn) == (other.player, other.pawn)
    
    def __hash__(self):
        return hash((self.player, self.pawn))
    
    def __repr__(self):
        print(f'{str(type(self))} -> {str(self.player)}, {str(self.pawn)}')

    # Abstract
    '''
    Abstract method. This method applies the action to the grid
    '''
    def apply(self, game):
        pass


# Following classes are the possible actions

class Spawn(Action):
    def __init__(self, player : Player, pawn : Pawn, spawn_col : int):
        super().__init__(player, pawn)
        if 0 <= spawn_col < N_COLS:
            self.position = Coord(player.spawn_row(), spawn_col)
        else:
            raise ValueError('Position must be a valid column')
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False 
        return (self.player, self.pawn, self.position) == (other.player, other.pawn, other.position)
    
    def __repr__(self):
        return f'Spawn {self.pawn.player.name} PAWN {self.pawn.number} IN {self.position}'
    
        
    def __hash__(self):
        return hash((self.player, self.pawn, self.position))

    def apply(self, game : Kulibrat):
        game.move_pawn(self.pawn, self.position)


class DiagonalMove(Action):
    def __init__(self, player : Player, pawn : Pawn, direction):
        '''
        Direction could be WEST or EAST
        '''
        super().__init__(player, pawn)
        self.dest = Coord(pawn.position.row + player.row_dir(), pawn.position.col + direction)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False 
        return (self.player, self.pawn, self.dest) == (other.player, other.pawn, other.dest)

    def apply(self, game : Kulibrat):
        game.move_pawn(self.pawn, self.dest)
    
    def __hash__(self):
        return hash((self.player, self.pawn, self.dest))
    
        
    def __repr__(self):
        return f'MOVE PAWN {str(self.pawn.number)} FROM {self.pawn.position} TO {self.dest}'


class Attack(Action):
    def __init__(self, player : Player, pawn : Pawn):
        super().__init__(player, pawn)
        self.dest = Coord(pawn.position.row + player.row_dir(), pawn.position.col)
    
    def apply(self, game : Kulibrat):
        game.move_pawn(self.pawn, self.dest)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False 
        return (self.player, self.pawn, self.dest) == (other.player, other.pawn, other.dest)
    
    def __hash__(self):
        return hash((self.player, self.pawn, self.dest))

    def __repr__(self):
        return f'ATTACK POSITION {self.dest} WITH PAWN {str(self.pawn.number)}'


class Jump(Action):
    def __init__(self, player : Player, pawn : Pawn, jump: int):
        '''
        jump contains the difference between the starting column and the destination column.
        For Red players that value is always negative
        '''
        super().__init__(player, pawn)
        self.jump = jump
        self.dest = Coord(pawn.position.row + jump, pawn.position.col)
    
    def apply(self, game):
        game.move_pawn(self.pawn, self.dest)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False 
        return (self.player, self.pawn, self.dest) == (other.player, other.pawn, other.dest)
    
    def __hash__(self):
        return hash((self.player, self.pawn, self.dest))
    
    def __repr__(self):
        return f'JUMP TO {str(self.dest)} WITH PAWN {str(self.pawn.number)}'



class Kulibrat(object):
    '''
    Game State class.

    Contains all the data structure for keeping the game state and modifying it.
    '''
    def __init__(self,max_score : int = 5):
        ''' Grid arrangement
        (-1,0) (-1,1) (-1,2)  # RED GOAL COORDINATES
        (0,0)  (0,1)  (0,2) 
        (1,0)  (1,1)  (1,2)
        (2,0)  (2,1)  (2,2)
        (3,0)  (3,1)  (3,2)
        (4,0)  (4,1)  (4,2)   # BLACK GOAL COORDINATES
        '''  
        self.grid = Grid()
        self.turn : Player = Player.BLACK
        self.score = {Player.BLACK : 0, Player.RED : 0}
        self.pawns = {Player.BLACK : [Pawn(Player.BLACK, i) for i in range(N_PAWNS)], Player.RED : [Pawn(Player.RED, i) for i in range(N_PAWNS)]}
        self.allowed_actions = self.get_possible_actions()
        self.max_score = max_score
        self.winner = Player.EMPTY

    def copy_state(self) -> Kulibrat:
        new = Kulibrat(max_score=self.max_score)
        new.pawns = {Player.BLACK : [pawn.copy() for pawn in self.pawns[Player.BLACK]], Player.RED  : [pawn.copy() for pawn in self.pawns[Player.RED]]}
        new.grid = Grid.grid_from_pawns(new.pawns)
        new.turn = copy.deepcopy(self.turn)
        new.score = copy.deepcopy(self.score)
        new.winner = copy.deepcopy(self.winner)
        new.allowed_actions = new.get_possible_actions()
        return new

    
    def __eq__(self, other) -> bool: 
        if type(self) != type(other):
            return False 
        return (self.grid, self.turn, self.score, self.pawns, self.max_score) == (other.player, other.turn, other.score, other.pawns, other.max_score)

    def check_valid_coord(self, coord):
        return 0 <= coord.row < N_ROWS and 0 <= coord.col < N_COLS
    
    def get_pawns_by_player(self, player : Player) -> List[Pawn]:
        return self.pawns[player]
    
    def get_pawn_by_id(self, player, number) -> Pawn:
        return self.pawns[player][number]
    
    def check_game_over(self):
        return self.winner != Player.EMPTY
    
    def pre_turn(self, action : Action):
        if self.winner != Player.EMPTY:
            raise ValueError('Game has ended')
        if self.turn != action.player:
            raise ValueError('It is not the turn of the player')
        if action not in self.allowed_actions:
            raise ValueError(f'Forbidden move {str(action)}, allowed actions {self.get_possible_actions()}')
    
    
    def post_turn(self):
        # Check and score points (1 point == 1 pawn in the goal column)
        for col in range(N_COLS):
            goal_cell = self.grid[self.turn.goal_row(), col]
            if goal_cell.player == self.turn:
                self.score[self.turn] += 1
                goal_cell.position = None
                self.grid[self.turn.goal_row(), col] = Pawn(Player.EMPTY)
        # Check winning by reaching max score
        if self.score[self.turn] >= self.max_score:
            self.winner = self.turn
            return
        # Switch turn
        self.turn = self.turn.opponent()
        self.allowed_actions = self.get_possible_actions()
        # If no actions possible switch turn againKulibrat
        if len(self.allowed_actions) == 0:
            self.turn = self.turn.opponent()
            self.allowed_actions = self.get_possible_actions()
            # If no action possible after the switch then the last to move loses
            if len(self.allowed_actions) == 0:
                self.winner = self.turn
                self.score[self.turn] = self.max_score
                return

    def move_pawn(self, pawn_ : Pawn, dest : Coord):

        if pawn_.player is not None and pawn_.player != Player.EMPTY and pawn_.number is not None:
            pawn = self.pawns[pawn_.player][pawn_.number]
        else:
            raise ValueError('None pawn are not accepted')

        start_pos = pawn.position

        dest_pawn = self.grid[dest]
        if dest_pawn.is_placed():
            dest_pawn.position = None
        pawn.position = dest

        if start_pos is not None:
            self.grid[start_pos] = Pawn(Player.EMPTY)
        self.grid[dest] = pawn
        

    def execute_action(self, action : Action) -> None:
        '''
        Executes the provided action executing the pre turn checks and post turn computations
        1) Pre turn validates the move
        2) The action is executed
        3) Post turn updates the game status and checks the next turn available moves
        '''
        self.pre_turn(action)
        action.apply(self)
        self.post_turn()

    def get_possible_actions(self) -> List[Action]:
        '''
        Calculates all the legal actions with regard to the current state of the game
        '''
        actions = []
        # Spawn moves
        spawn_pawn_n = min((i for i in range(N_PAWNS) if self.get_pawn_by_id(self.turn, i).position is None), default=None) 
        if spawn_pawn_n is not None: # If all pawns are not used
            spawn_pawn = self.get_pawn_by_id(self.turn, spawn_pawn_n)   # Pawn to spawn (the unused one with the lowest id)
            for col in range(N_COLS):        
                if self.grid[spawn_pawn.player.spawn_row(), col].is_empty():
                    actions.append(Spawn(self.turn, spawn_pawn, col))
        
        # Diagonal moves
        for pawn in self.get_pawns_by_player(self.turn):    
            if pawn.is_placed():
                for col_move_dir in [EAST, WEST]: # -1 and 1
                    dest = pawn.position + (pawn.player.row_dir(), col_move_dir)
                    if not (self.check_valid_coord(dest) or self.turn.check_goal_coord(dest)):
                        continue
                    if not self.grid[dest].is_empty():
                        continue
                    actions.append(DiagonalMove(self.turn, pawn, col_move_dir))
        
        #Attack
        for pawn in self.get_pawns_by_player(self.turn):
            if pawn.is_placed():
                dest = pawn.position + (pawn.player.row_dir(), 0)
                if not (self.check_valid_coord(dest) or self.turn.check_goal_coord(dest)):
                    continue
                if self.grid[dest].is_empty():
                    continue
                if self.grid[dest].player != self.turn:
                    actions.append(Attack(self.turn, pawn))
        
        #Jump
        for pawn in self.get_pawns_by_player(self.turn):
            if pawn.is_placed():
                d_row = self.turn.row_dir()
                dest = pawn.position + (d_row, 0)
                # Check if the next is occupied
                if not (self.check_valid_coord(dest) or self.turn.check_goal_coord(dest)):
                    continue
                if self.grid[dest].is_empty() or self.grid[dest].player == self.turn:
                    continue
                while (self.check_valid_coord(dest) or self.turn.check_goal_coord(dest)):
                    d_row += pawn.player.row_dir()
                    dest = pawn.position + (d_row, 0)
                    if self.grid[dest].is_empty():
                        actions.append(Jump(self.turn, pawn, d_row))
                        break
                    if self.grid[dest].player == self.turn:
                        break
        return actions

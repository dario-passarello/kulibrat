from collections import namedtuple
from typing import List

EMPTY = -1
BLACK = 0
RED = 1

EAST = -1
WEST = 1



# Color EMPTY means no pawn in the square
# WHen color is EMPTY, the number is unspecified
Pawn = namedtuple('Pawn', ['color', 'number'])
Coord = namedtuple('Coord', ['row','col'])


class Action:
    def __init__(self, player):
        self.player = player

    def apply(self, game):
        pass

#player (black or red)
#type
#start (could be none)
#direction (is LEFT or RIGHT)
class DiagonalMove(Action):
    def __init__(self, player, start, direction):
        super().__init__(player)
        self.start = start
        self.direction = direction
    
    def apply(self, game):
        if game.grid[self.start].color != self.player:
            raise ValueError(f'Wrong pawn type selected for the move')
        if self.player == BLACK:
            drow = -1
        elif self.player == RED:
            drow = 1
        else:
            raise ValueError('Player must be BLACK or RED')
        destination = Coord(drow, self.direction)
        # TODO check of valid coordinate
        # Check if point if scored 
        # Check that destination is free
        # Apply move to the grid

    


class Kulibrat(object):
    def __init__(self):
        ''' Grid arrangement
        (0,0) (0,1) (0,2) 
        (1,0) (1,1)
        (2,0)
        (3,0)
        '''
        self.grid = {(i,j) : Pawn(EMPTY, None) for i in range(4) for j in range(3)}
        self.turn = BLACK
        self.score = (0, 0)
        self.pawns_out = {Pawn(BLACK, i) for i in range(4)}  | {Pawn(RED, i) for i in range(4)}
    
    @staticmethod
    def check_valid_coord(coord):
        return 0 <= coord.row < 4 and 0 <= coord.col < 3

    
    def get_possible_moves(self) -> List[Move]:
        pass

    def apply_move(self, move : Move):
        move.apply()


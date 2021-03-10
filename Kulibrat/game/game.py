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
Coord = namedtuple('Coord', ['row', 'col'])

#to keep tracks on number of pawns, 0 meaning there is no that pawn on the board
#but still not used
pawnnubmersB =[0,0,0,0]
pawnnubmersR =[0,0,0,0]

class Action:
    def __init__(self, player, pawn):
        self.player = player
        self.pawn = pawn

    def apply(self, game):
        pass


# TODO finish spawn class
#check when is possilbe and apply, and update grid and number/s of pawn/s

#player(black or red),puting new pawn and position as (i,j) if possible
class Spawn(Action):
    def __init__(self, player,position):
        super().__init__(player)
        self.position = position

    def apply(self, game):
        pass


# player (black or red)
# type
# start (could be none)
# direction (east or west)
class DiagonalMove(Action):
    def __init__(self, player, pawn, start, direction):
        super().__init__(player)
        super().__init__(pawn)
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

        destination = Coord(self.pawn.row + drow, self.pawn.col + self.direction)

        # for black player
        if self.player == BLACK:
            # check if black player is in on a last row, because then will score
            if game.grid[self.start.row] == 3:
                self.score[0] += 1
                #updating grid
                self.grid[self.start.row][self.start.col] = EMPTY
                if self.grid[destination] == EMPTY:
                    #updating position of pawn
                    self.pawn.row = destination[0]
                    self.pawn.col = destination[1]
        # for red player
        elif self.player == RED:
            # check if red player is in on a first row, because then will score
            if game.grid[self.start.col] == 0:
                self.score[1] += 1
                # updating grid
                self.grid[self.start.row][self.start.col] = EMPTY
                #Check that destination is free
                if self.grid[destination] == EMPTY:
                    #updating position of pawn
                    self.pawn.row = destination[0]
                    self.pawn.col = destination[1]


        # TODO check of valid coordinate
        #for diagonal move:
        # Check for scoring - done
        # Check that destination is free- done
        # Apply move to the grid - done




class Kulibrat(object):
    def __init__(self):
        ''' Grid arrangement
        (0,0) (0,1) (0,2) 
        (1,0) (1,1)
        (2,0)
        (3,0)
        '''
        self.grid = {(i, j): Pawn(EMPTY, None) for i in range(4) for j in range(3)}
        self.turn = BLACK
        self.score = (0, 0)
        self.pawns_out = {Pawn(BLACK, i) for i in range(4)} | {Pawn(RED, i) for i in range(4)}

    @staticmethod
    def check_valid_coord(coord):
        return 0 <= coord.row < 4 and 0 <= coord.col < 3

    # def get_possible_moves(self) -> List[Move]:
    #    pass

    # def apply_move(self, move : Move):
    #    move.apply()


def board(grid):
    boardlist=[]
    for i in range(4):
        for j in range(3):
            cordinate = Coord(i, j)
            if grid[cordinate].color == EMPTY:
                boardlist.append("X")
            if grid[cordinate].color == BLACK:
                boardlist.append("B",grid[cordinate].number)
            if grid[cordinate].color == RED:
                boardlist.append("R",grid[cordinate].number)
        print(boardlist)
        boardlist = []


game = Kulibrat()
print(board(game.grid))
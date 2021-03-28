from Kulibrat.game.game import Kulibrat, Pawn, Player
import Kulibrat.game.game as Game


row_header = "   " + " {} " * Game.N_COLS
row_separator = "  x" + "--x" * Game.N_COLS
row_format = "{} |" + "{}|" * Game.N_COLS


def display_pawn(pawn: Pawn) -> str:
    rep = ""
    if pawn.player == Player.EMPTY:
        return "  "

    if pawn.player == Player.BLACK:
        rep += "B"
    elif pawn.player == Player.RED:
        rep += "R"

    rep += str(pawn.number)

    return rep


def draw_grid(game: Kulibrat):
    print(row_header.format(*(range(Game.N_COLS + 1))))
    print(row_separator)
    for i, row in enumerate(game.grid.rows()):
        display_row = [str(i)] + [display_pawn(pawn) for pawn in row]
        print(row_format.format(*display_row))
        print(row_separator)
    print()

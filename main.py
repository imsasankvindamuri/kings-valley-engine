from typing import TypeAlias
import random


# ============================================================
# Types
# ============================================================

Square: TypeAlias = tuple[int, int]
Move: TypeAlias = tuple[Square, Square]
Board: TypeAlias = list[list[int]]

# ============================================================
# Constants
# ============================================================

WHITE_TURN = 1
BLACK_TURN = -1

FILES = "abcde"

PIECES = {
    0: ".",
    1: "♖",    # White Servant
    2: "♔",    # White Pharaoh
   -1: "♜",    # Black Servant
   -2: "♚",    # Black Pharaoh
}

INITIAL_BOARD: Board = [
    [-1, -1, -2, -1, -1],
    [ 0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0],
    [ 1,  1,  2,  1,  1],
]

KING_VALLEY = (
    len(INITIAL_BOARD) // 2,
    len(INITIAL_BOARD[0]) // 2,
)

# ============================================================
# Coordinate Helpers
# ============================================================

def square_to_str(square: Square) -> str:
    r, c = square
    return f"{FILES[c]}{5-r}"


def str_to_square(text: str) -> Square:
    text = text.lower()

    file = FILES.index(text[0])
    rank = int(text[1])

    return (5-rank, file)


def move_to_str(move: Move) -> str:
    start, end = move
    return square_to_str(start) + square_to_str(end)


# ============================================================
# Board Display
# ============================================================

def print_board(board: Board) -> None:
    print()
    print("  a b c d e")

    for r in range(5):
        rank = 5 - r

        row = []

        for c in range(5):

            if (r, c) == KING_VALLEY and board[r][c] == 0:
                row.append("X")
            else:
                row.append(PIECES[board[r][c]])

        print(rank, " ".join(row))

    print()


# ============================================================
# Move Generation
# ============================================================

def generate_moves(turn: int, board: Board) -> list[Move]:
    """
    turn =  1 -> White
    turn = -1 -> Black
    """

    nrows = len(board)
    ncols = len(board[0])

    moves: list[Move] = []

    directions = [
        (-1, 0),  # up
        ( 1, 0),  # down
        ( 0,-1),  # left
        ( 0, 1),  # right
    ]

    for r in range(nrows):
        for c in range(ncols):

            piece = board[r][c]

            if piece == 0:
                continue

            if piece * turn <= 0:
                continue

            is_pharaoh = abs(piece) == 2

            for dr, dc in directions:

                cr, cc = r, c

                while True:
                    nr = cr + dr
                    nc = cc + dc

                    if not (0 <= nr < nrows and 0 <= nc < ncols):
                        break

                    if board[nr][nc] != 0:
                        break

                    cr, cc = nr, nc

                if (cr, cc) == (r, c):
                    continue

                # Servants may not occupy the valley.
                if not is_pharaoh and (cr, cc) == KING_VALLEY:
                    continue

                moves.append(((r, c), (cr, cc)))

    return moves


# ============================================================
# Move Application
# ============================================================

def apply_move(board: Board, move: Move) -> Board:
    (r1, c1), (r2, c2) = move

    new_board = [row[:] for row in board]

    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = 0

    return new_board


# ============================================================
# Win Detection
# ============================================================

def winner(board: Board) -> int | None:
    piece = board[KING_VALLEY[0]][KING_VALLEY[1]]

    if piece == 2:
        return WHITE_TURN

    if piece == -2:
        return BLACK_TURN

    return None


# ============================================================
# Input Parsing
# ============================================================

def parse_move(text: str) -> Move:
    """
    Examples:
        c1c4
        a1a4
        e5e2
    """

    text = text.strip().lower()

    if len(text) != 4:
        raise ValueError("Move must have length 4.")

    return (
        str_to_square(text[:2]),
        str_to_square(text[2:]),
    )


# ============================================================
# Main Game Loop
# ============================================================

def play_game(white_is_human: bool = True, black_is_human: bool = True):
    board = [row[:] for row in INITIAL_BOARD]

    turn = WHITE_TURN

    while True:

        print_board(board)

        result = winner(board)

        if result == WHITE_TURN:
            print("White wins!")
            return

        if result == BLACK_TURN:
            print("Black wins!")
            return

        legal_moves = generate_moves(turn, board)

        if not legal_moves:
            print("No legal moves. It's a draw!")
            return

        player_name = "White" if turn == WHITE_TURN else "Black"
        is_human = white_is_human if turn == WHITE_TURN else black_is_human

        print(f"{player_name} to move ({'Human' if is_human else 'Engine'})\n")

        if is_human:
            print("Legal moves:")
            for move in legal_moves:
                print(" ", move_to_str(move))

            while True:
                try:
                    text = input("\nMove: ")
                    move = parse_move(text)
                    if move not in legal_moves:
                        print("Illegal move.")
                        continue
                    break
                except Exception:
                    print("Invalid move format. Use e.g. 'c1c4'")
        else:
            # Engine move
            move = get_random_move(turn, board)
            print(f"Engine chooses: {move_to_str(move)}")

        board = apply_move(board, move)
        turn *= -1


# ============================================================
# AI Agents
# ============================================================

def get_random_move(turn: int, board: Board) -> Move:
    legal_moves = generate_moves(turn, board)
    return random.choice(legal_moves)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    print("Welcome to King's Valley!")
    print("1. Human vs Human")
    print("2. Human (White) vs Engine (Black)")
    print("3. Engine (White) vs Human (Black)")
    
    choice = input("\nSelect mode (1-3): ").strip()

    if choice == "1":
        play_game(white_is_human=True, black_is_human=True)
    elif choice == "2":
        play_game(white_is_human=True, black_is_human=False)
    elif choice == "3":
        play_game(white_is_human=False, black_is_human=True)
    else:
        print("Invalid choice. Starting Human vs Human by default.")
        play_game(white_is_human=True, black_is_human=True)

from typing import TypeAlias
import math

Square: TypeAlias = tuple[int, int]
Move: TypeAlias = tuple[Square, Square]
Board: TypeAlias = list[list[int]]

WHITE = 1
BLACK = -1
WINNING_EVAL = 10**6
LOSING_EVAL  = -10**6

FILES = "abcdefghijk"

PIECES = {
    0: ".",
    1: "♖",    # White Servant
    2: "♔",    # White Pharaoh
   -1: "♜",    # Black Servant
   -2: "♚",    # Black Pharaoh
}

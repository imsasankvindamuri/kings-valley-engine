from .types import Board, Square, Move, WHITE, BLACK, FILES, PIECES

class GameBoard:
    def __init__(self, size: int = 5):
        self.size = size
        self.valley = (size // 2, size // 2)
        self.board = self._create_initial_board(size)
        self.history = []
        self._record_state()

    def _create_initial_board(self, size: int) -> Board:
        board = [[0 for _ in range(size)] for _ in range(size)]
        # Black pieces (top)
        for c in range(size):
            board[0][c] = -2 if c == size // 2 else -1
        # White pieces (bottom)
        for c in range(size):
            board[size-1][c] = 2 if c == size // 2 else 1
        return board

    def _get_state_tuple(self):
        return tuple(tuple(row) for row in self.board)

    def _record_state(self):
        self.history.append(self._get_state_tuple())

    def is_threefold_repetition(self) -> bool:
        current_state = self._get_state_tuple()
        return self.history.count(current_state) >= 3

    def print(self):
        print()
        header = "  " + " ".join(FILES[:self.size])
        print(header)
        for r in range(self.size):
            rank = self.size - r
            row = []
            for c in range(self.size):
                if (r, c) == self.valley and self.board[r][c] == 0:
                    row.append("X")
                else:
                    row.append(PIECES[self.board[r][c]])
            rank_str = f"{rank:2}" if self.size > 9 else f"{rank}"
            print(f"{rank_str} {' '.join(row)}")
        print()

    def generate_moves(self, color: int) -> list[Move]:
        moves: list[Move] = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(self.size):
            for c in range(self.size):
                piece = self.board[r][c]
                if piece == 0 or piece * color <= 0:
                    continue
                is_pharaoh = abs(piece) == 2
                for dr, dc in directions:
                    cr, cc = r, c
                    while True:
                        nr, nc = cr + dr, cc + dc
                        if not (0 <= nr < self.size and 0 <= nc < self.size):
                            break
                        if self.board[nr][nc] != 0:
                            break
                        cr, cc = nr, nc
                    if (cr, cc) == (r, c):
                        continue
                    if not is_pharaoh and (cr, cc) == self.valley:
                        continue
                    moves.append(((r, c), (cr, cc)))
        return moves

    def apply_move(self, move: Move):
        (r1, c1), (r2, c2) = move
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = 0
        self._record_state()

    def get_winner(self) -> int | None:
        piece = self.board[self.valley[0]][self.valley[1]]
        if piece == 2: return WHITE
        if piece == -2: return BLACK
        return None

    def find_pharaoh(self, color: int) -> Square:
        target = 2 * color
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == target:
                    return (r, c)
        raise ValueError("Pharaoh not found")

def square_to_str(square: Square, size: int) -> str:
    r, c = square
    return f"{FILES[c]}{size - r}"

def str_to_square(text: str, size: int) -> Square:
    file = FILES.index(text[0].lower())
    rank = int(text[1:])
    return (size - rank, file)

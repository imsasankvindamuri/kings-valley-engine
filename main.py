from kings_valley.board import GameBoard, str_to_square, square_to_str
from kings_valley.engine import get_best_move
from kings_valley.types import WHITE, BLACK

def parse_move_input(text: str, size: int):
    mid = 0
    for i in range(1, len(text)):
        if text[i].isalpha():
            mid = i
            break
    return str_to_square(text[:mid], size), str_to_square(text[mid:], size)

def play_game(size: int, w_human: bool, b_human: bool):
    game = GameBoard(size)
    turn = WHITE

    while True:
        game.print()
        
        winner = game.get_winner()
        if winner:
            print(f"{'White' if winner == WHITE else 'Black'} wins!")
            return

        if game.is_threefold_repetition():
            print("Draw by threefold repetition!")
            return

        moves = game.generate_moves(turn)
        if not moves:
            print("Draw!")
            return

        is_human = w_human if turn == WHITE else b_human
        name = "White" if turn == WHITE else "Black"
        
        print(f"{name}'s turn ({'Human' if is_human else 'Engine'})")

        if is_human:
            while True:
                try:
                    text = input("Move (e.g. c1c4): ").strip()
                    move = parse_move_input(text, size)
                    if move in moves: break
                    print("Illegal.")
                except: print("Invalid.")
        else:
            print("Thinking...")
            move = get_best_move(game, turn, depth=4 if size <= 5 else 3)
            print(f"Engine chose: {square_to_str(move[0], size)}{square_to_str(move[1], size)}")

        game.apply_move(move)
        turn *= -1

if __name__ == "__main__":
    print("Welcome to King's Valley!")
    size = int(input("Size (5, 7, 9, 11) [5]: ") or 5)
    print("1. H v H\n2. H v E\n3. E v H\n4. E v E")
    choice = input("Choice: ")
    
    modes = {"1": (True, True), "2": (True, False), "3": (False, True), "4": (False, False)}
    w_h, b_h = modes.get(choice, (True, True))
    play_game(size, w_h, b_h)

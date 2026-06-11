import random
import copy
from .types import Board, Move, WHITE, BLACK, WINNING_EVAL, LOSING_EVAL
from .board import GameBoard

def manhattan(a, b):
    return abs(b[1] - a[1]) + abs(b[0] - a[0])

def evaluate(game: GameBoard) -> float:
    winner = game.get_winner()
    if winner is not None:
        return winner * WINNING_EVAL
    
    w_pos = game.find_pharaoh(WHITE)
    b_pos = game.find_pharaoh(BLACK)
    
    return manhattan(game.valley, b_pos) - manhattan(game.valley, w_pos)

def minimax(game: GameBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
    winner = game.get_winner()
    if winner is not None:
        return winner * WINNING_EVAL
    
    if depth == 0:
        return evaluate(game)

    if is_maximizing:
        best_score = LOSING_EVAL
        for move in game.generate_moves(WHITE):
            # Use copy for simulation to avoid corrupting actual board
            temp_game = copy.deepcopy(game)
            temp_game.apply_move(move)
            score = minimax(temp_game, depth - 1, False, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = WINNING_EVAL
        for move in game.generate_moves(BLACK):
            temp_game = copy.deepcopy(game)
            temp_game.apply_move(move)
            score = minimax(temp_game, depth - 1, True, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def get_best_move(game: GameBoard, turn: int, depth: int) -> Move:
    legal_moves = game.generate_moves(turn)
    if not legal_moves:
        raise ValueError("No moves")
    
    best_move = random.choice(legal_moves)
    
    if turn == WHITE:
        best_score = LOSING_EVAL
        for move in legal_moves:
            temp_game = copy.deepcopy(game)
            temp_game.apply_move(move)
            score = minimax(temp_game, depth - 1, False, LOSING_EVAL, WINNING_EVAL)
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = WINNING_EVAL
        for move in legal_moves:
            temp_game = copy.deepcopy(game)
            temp_game.apply_move(move)
            score = minimax(temp_game, depth - 1, True, LOSING_EVAL, WINNING_EVAL)
            if score < best_score:
                best_score = score
                best_move = move
                
    return best_move

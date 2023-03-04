import book
import chess
from evaluation import evaluate_board, evaluate_move

MATE_SCORE = 1000000000
MATE_THRESHOLD = 999000000


def calculate_best_move(depth: int, board: chess.Board) -> chess.Move:
    """
    Calculates and returns the next best move
    :param depth:
    :param board:
    :return:
    """

    if book_move := book.search_move_book(board):
        return book_move
    else:
        return minimax_root(depth, board)


def calculate_ordered_moves(board: chess.Board):
    """
    Of all legal moves, orders them from best to worst
    :param board:
    :return:
    """

    def order_key(move):  # Key for sorted function returns the move evaluation
        return evaluate_move(board, move)

    ordered_moves = sorted(board.legal_moves, key=order_key, reverse=(board.turn == chess.WHITE))

    return list(ordered_moves)


def minimax_root(depth: int, board: chess.Board) -> chess.Move:
    """
    What is the highest value move per our evaluation function?
    """
    # White always wants to maximize (and black to minimize)
    # the board score according to evaluate_board()
    maximize = board.turn
    best_move = -float("inf") if maximize else float("inf")
    moves = calculate_ordered_moves(board)
    best_move_found = moves[0]

    for move in moves:
        board.push(move)
        if board.can_claim_draw():
            value = 0.0
        else:
            value = minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        if maximize and value >= best_move or not maximize and value <= best_move:
            best_move = value
            best_move_found = move
    return best_move_found


# Took this from another engine if I'm going to be honest
def minimax(depth: int, board: chess.Board, alpha: float, beta: float, is_maximising_player: bool) -> float:
    if board.is_checkmate():  # If the previous move resulted in checkmate
        return -MATE_SCORE if is_maximising_player else MATE_SCORE
    # When the game is over and it's not a checkmate it's a draw
    # In this case, don't evaluate. Just return a neutral result: zero
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    moves = calculate_ordered_moves(board)
    if is_maximising_player:
        best_move = -float("inf")
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            # Each ply after a checkmate is slower, so they get ranked slightly less
            # We want the fastest mate!
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = max(
                best_move,
                curr_move,
            )
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
    else:
        best_move = float("inf")
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1, board, alpha, beta, not is_maximising_player)
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = min(
                best_move,
                curr_move,
            )
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move

    return best_move

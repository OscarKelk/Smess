import chess
from move_choice import calculate_best_move


def render(board: chess.Board) -> str:
    """
    Print a side-relative chess board with special chess characters.
    """
    board_string = list(str(board))
    uni_pieces = {
        "R": "♖",
        "N": "♘",
        "B": "♗",
        "Q": "♕",
        "K": "♔",
        "P": "♙",
        "r": "♜",
        "n": "♞",
        "b": "♝",
        "q": "♛",
        "k": "♚",
        "p": "♟",
        ".": "·",
    }
    for idx, char in enumerate(board_string):
        if char in uni_pieces:
            board_string[idx] = uni_pieces[char]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    display = []
    for rank in "".join(board_string).split("\n"):
        display.append(f"  {ranks.pop()} {rank}")
    if board.turn == chess.BLACK:
        display.reverse()
    display.append("    a b c d e f g h")
    return "\n" + "\n".join(display)


run_game = True

board = chess.Board()
while run_game:
    if not board.is_game_over():  # While game is ongoing
        print(render(board))

        while True:
            move = input(">> ")
            try:
                board.push_san(move)
                break
            except chess.IllegalMoveError:
                print("Illegal move, try again")
            except chess.InvalidMoveError:
                print("Invalid move, try again")

        engine_move = calculate_best_move(3, board)
        if engine_move:
            board.push(engine_move)
        else:
            print(f"{board.outcome().termination}! {board.outcome().winner} win(s).")

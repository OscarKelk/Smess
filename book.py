import chess
import json
import random

default_book_path = r"C:\Users\oscar\Desktop\Personal\Software\Python\Smess\book.json"


def search_move_book(board: chess.Board, book_path: str = default_book_path) -> chess.Move | bool:
    """Returns a move from the book if possible"""

    with open(book_path, "r") as f:
        move_book = json.load(f)
    try:
        # Try to find a move in the book
        fen = board.fen()
        move = chess.Move.from_uci(random.choice(move_book[fen]))
        return move
    except KeyError:
        try:
            # Let's try again, with a fen without ep allowed
            fen = board.fen()
            fen = fen.split()
            fen[-3] = '-'
            fen = ' '.join(fen)
            move = chess.Move.from_uci(random.choice(move_book[fen]))
            return move
        except KeyError:
            return False

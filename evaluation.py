import chess

weights = {chess.PAWN: 100, chess.KNIGHT: 280, chess.BISHOP: 320, chess.ROOK: 479, chess.QUEEN: 929, chess.KING: 60000}
pst = {
    chess.WHITE: {
        chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0,
                     78, 83, 86, 73, 102, 82, 85, 90,
                     7, 29, 21, 44, 40, 31, 44, 7,
                     -17, 16, -2, 15, 14, 0, 15, -13,
                     -26, 3, 10, 9, 6, 1, 0, -23,
                     -22, 9, 5, -11, -10, -2, 3, -19,
                     -31, 8, -7, -37, -36, -14, 3, -31,
                     0, 0, 0, 0, 0, 0, 0, 0],
        chess.KNIGHT: [-66, -53, -75, -75, -10, -55, -58, -70,
                       -3, -6, 100, -36, 4, 62, -4, -14,
                       10, 67, 1, 74, 73, 27, 62, -2,
                       24, 24, 45, 37, 33, 41, 25, 17,
                       -1, 5, 31, 21, 22, 35, 2, 0,
                       -18, 10, 13, 22, 18, 15, 11, -14,
                       -23, -15, 2, 0, 2, 0, -23, -20,
                       -74, -23, -26, -24, -19, -35, -22, -69],
        chess.BISHOP: [-59, -78, -82, -76, -23, -107, -37, -50,
                       -11, 20, 35, -42, -39, 31, 2, -22,
                       -9, 39, -32, 41, 52, -10, 28, -14,
                       25, 17, 20, 34, 26, 25, 15, 10,
                       13, 10, 17, 23, 17, 16, 0, 7,
                       14, 25, 24, 15, 8, 25, 20, 15,
                       19, 20, 11, 6, 7, 6, 20, 16,
                       -7, 2, -15, -12, -14, -15, -10, -10],
        chess.ROOK: [35, 29, 33, 4, 37, 33, 56, 50,
                     55, 29, 56, 67, 55, 62, 34, 60,
                     19, 35, 28, 33, 45, 27, 25, 15,
                     0, 5, 16, 13, 18, -4, -9, -6,
                     -28, -35, -16, -21, -13, -29, -46, -30,
                     -42, -28, -42, -25, -25, -35, -26, -46,
                     -53, -38, -31, -26, -29, -43, -44, -53,
                     -30, -24, -18, 5, -2, -18, -31, -32],
        chess.QUEEN: [6, 1, -8, -104, 69, 24, 88, 26,
                      14, 32, 60, -10, 20, 76, 57, 24,
                      -2, 43, 32, 60, 72, 63, 43, 2,
                      1, -16, 22, 17, 25, 20, -13, -6,
                      -14, -15, -2, -5, -1, -10, -20, -22,
                      -30, -6, -13, -11, -16, -11, -16, -27,
                      -36, -18, 0, -19, -15, -15, -21, -38,
                      -39, -30, -31, -13, -31, -36, -34, -42],
        "king": [4, 54, 47, -99, -99, 60, 83, -62,
                 -32, 10, 55, 56, 56, 55, 10, 3,
                 -62, 12, -57, 44, -67, 28, 37, -31,
                 -55, 50, 11, -4, -19, 13, 0, -49,
                 -55, -43, -52, -28, -51, -47, -8, -50,
                 -47, -42, -43, -79, -64, -32, -29, -32,
                 -4, 3, -14, -50, -57, -18, 13, 4,
                 17, 30, -3, -14, 6, -1, 40, 18],
        "king_endgame": [50, -30, -30, -30, -30, -30, -30, -50,
                         -30, -30, 0, 0, 0, 0, -30, -30,
                         -30, -10, 20, 30, 30, 20, -10, -30,
                         -30, -10, 30, 40, 40, 30, -10, -30,
                         -30, -10, 30, 40, 40, 30, -10, -30,
                         -30, -10, 20, 30, 30, 20, -10, -30,
                         -30, -20, -10, 0, 0, -10, -20, -30,
                         -50, -40, -30, -20, -20, -30, -40, -50]
    }
}

pst[chess.BLACK] = {
    chess.PAWN: list(reversed(pst[chess.WHITE][chess.PAWN])),
    chess.KNIGHT: list(reversed(pst[chess.WHITE][chess.KNIGHT])),
    chess.BISHOP: list(reversed(pst[chess.WHITE][chess.BISHOP])),
    chess.ROOK: list(reversed(pst[chess.WHITE][chess.ROOK])),
    chess.QUEEN: list(reversed(pst[chess.WHITE][chess.QUEEN])),
    "king": list(reversed(pst[chess.WHITE]["king"])),
    "king_endgame": list(reversed(pst[chess.WHITE]["king_endgame"]))
}


def evaluate_piece(piece: chess.Piece, square: chess.Square, endgame: bool) -> int:
    if piece.piece_type == chess.KING:
        table = pst[piece.color]["king_endgame"] if endgame else pst[piece.color]["king"]
    else:
        table = pst[piece.color][piece.piece_type]

    return table[square]


def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
    if board.is_en_passant(move):
        return weights[chess.PAWN]

    piece_capturing = board.piece_at(move.from_square).piece_type
    piece_captured = board.piece_at(move.to_square).piece_type

    return weights[piece_captured] - weights[piece_capturing]


def evaluate_move(board: chess.Board, move: chess.Move) -> float:
    endgame = check_endgame(board)
    piece_moved = board.piece_at(move.from_square)

    # Calculate the value of the piece's change in position between its last position and its new one
    from_piece_val = evaluate_piece(piece_moved, move.from_square, endgame)
    to_piece_val = evaluate_piece(piece_moved, move.to_square, endgame)
    pos_change = to_piece_val - from_piece_val

    capture_value = 0.0
    if board.is_capture(move):  # If there is a capture in the move, evaluate that
        capture_value = evaluate_capture(board, move)

    move_value = capture_value + pos_change

    if board.turn == chess.BLACK:
        move_value = -move_value

    return move_value


def evaluate_board(board: chess.Board) -> float:
    """
    Evaluates the entire board to determine which player has the current advantage.
    From white's perspective, so + is white, - is black
    :param board:
    :return float:
    """
    evaluation = 0.0
    endgame = check_endgame(board)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        piece_value = weights[piece.piece_type] + evaluate_piece(piece, square, endgame)
        if piece.color == chess.WHITE:
            evaluation += piece_value
        else:
            evaluation -= piece_value

    return evaluation


def check_endgame(board: chess.Board) -> bool:
    """
    Determines whether the game is in the endgame
    In endgame when:
    - Both sides have no queens or
    - Every side which has a queen has additionally no other pieces or one minorpiece maximum.
    Counts these pieces

    :param board:
    :return bool:
    """
    queens = 0
    minor_pieces = 0

    for square in chess.SQUARES:
        if piece := board.piece_at(square):
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                minor_pieces += 1

    return queens == 0 or (queens == 2 and minor_pieces <= 1)

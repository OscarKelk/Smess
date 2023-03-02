import chess.engine
import datetime
import move_choice


stockfish = chess.engine.SimpleEngine.popen_uci(r"C:\Users\oscar\Desktop\Personal\Applications\stockfish_15.1_win_x64_avx2\stockfish_15.1_win_x64_avx2\stockfish.exe")

board = chess.Board()
move_counter = 0
while not board.is_game_over():
    stockfish_move = stockfish.play(board, chess.engine.Limit(time=0.1))
    board.push(stockfish_move.move)
    print(stockfish_move.move)

    if board.is_game_over():
        break
    smess_move = move_choice.calculate_best_move(3, board)
    board.push(smess_move)
    print(smess_move)

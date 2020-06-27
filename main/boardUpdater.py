import random

from apscheduler.schedulers.background import BackgroundScheduler
import chess

from main.models import ChessBoard


def update_boards():
    chess_boards = ChessBoard.objects.all()
    for board_obj in chess_boards:
        board = chess.Board(board_obj.fen)
        if board.is_game_over():
            ChessBoard.objects.filter(id=board_obj.id).delete()
            continue
        legal_moves = list(board.legal_moves)
        random_index = random.randint(0, len(legal_moves) - 1)
        board.push(legal_moves[random_index])
        board_obj.fen = board.fen()
        board_obj.last_move = legal_moves[random_index].uci()
        board_obj.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_boards, 'interval', seconds=2)
    scheduler.start()
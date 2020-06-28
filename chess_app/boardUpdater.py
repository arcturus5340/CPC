import random

from apscheduler.schedulers.background import BackgroundScheduler
import chess

from chess_app.models import ChessBoard, PGN


def update_boards():
    chess_boards = ChessBoard.objects.all()
    for board_obj in chess_boards:
        board = chess.Board(board_obj.fen)
        if board.is_game_over():
            white_win = int((board.fen().split()[1] == 'b') and board.is_variant_loss())
            black_win = int((board.fen().split()[1] == 'w') and board.is_variant_loss())
            if white_win != black_win:
                result = '{}-{}'.format(white_win, black_win)
            else:
                result = '1/2-1/2'
            board_obj.pgn_meta += '\n[Result "{}"]\n'.format(result)
            ChessBoard.objects.filter(id=board_obj.id).delete()

            new_pgn_obj = PGN.objects.create()
            new_id = PGN.objects.latest('id').id
            with open('chess_reports/{}.pgn'.format(new_id), 'w') as file:
                file.write(board_obj.pgn_meta)
                file.write('\n')
                file.write(board_obj.moves)
                file.write(result)
            new_pgn_obj.src = 'chess_reports/{}.pgn'.format(new_id)
            new_pgn_obj.save()

            continue
        legal_moves = list(board.legal_moves)
        random_index = random.randint(0, len(legal_moves) - 1)
        board.push(legal_moves[random_index])
        board_obj.fen = board.fen()
        board_obj.moves += ((board.fen().split()[-1]+'.') if board.fen().split()[1] == 'b' else '') + legal_moves[random_index].uci() + ' '
        board_obj.save()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_boards, 'interval', seconds=2)
    scheduler.start()

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import datetime
import json
import random

import chess

from chess_app.models import ChessBoard, PGN


def index(request):
    context = {'ChessBoards': ChessBoard.objects.values_list('id', 'fen')}
    return render(request, 'index.html', context)


def add_board(request):
    event = '[Event "{}"]'.format('???')
    site = '[Site "{}"]'.format('???')
    now = datetime.datetime.now()
    date = '[Date "{}"]'.format(now.strftime('%Y.%m.%d'))
    round = '[Round "{}"]'.format('???')
    white_player = '[White "{}"]'.format(request.POST.get('white'))
    black_player = '[Black "{}"]'.format(request.POST.get('black'))

    white_hash = random.getrandbits(32)
    black_hash = random.getrandbits(32)
    ChessBoard.objects.create(pgn_meta='\n'.join([event, site, date, round, white_player, black_player]),
                              white=white_hash,
                              black=black_hash)

    response = {
        'chess_game_id': ChessBoard.objects.latest('id').id,
        'white_hash': white_hash,
        'black_hash': black_hash,
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


def update_boards(request):
    chess_boards = ChessBoard.objects.all()
    response = {'ChessBoards': dict()}
    for board in chess_boards:
        response['ChessBoards'][board.id] = board.fen
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_fen(request, board_id):
    response = {'FEN': ChessBoard.objects.get(id=board_id).fen}
    return JsonResponse(response, content_type='application/json')


def move(request, player_hash, move_uci):
    response = dict()
    board_obj = ChessBoard.objects.get(Q(white__exact=player_hash) | Q(black__exact=player_hash))
    board = chess.Board(board_obj.fen)

    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        board_obj.fen = board.fen()
        board_obj.moves += ((board.fen().split()[-1]+'.') if board.fen().split()[1] == 'b' else '') + move_uci + ' '
        board_obj.save()

        if board.is_game_over():
            white_win = int((board.turn == chess.BLACK) and board.is_variant_loss())
            black_win = int((board.turn == chess.WHITE) and board.is_variant_loss())
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

            response['status'] = 'successful'
            return JsonResponse(response)

        response['status'] = 'successful'
    else:
        response['status'] = 'fail'
        response['message'] = 'Invalid move ({})'.format(move_uci)

    return JsonResponse(response)

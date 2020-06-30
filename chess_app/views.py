from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import datetime
import json
import random

import chess
import chess.pgn

from chess_app.models import ChessBoard, PGN


def index(request):
    context = {'ChessBoards': ChessBoard.objects.values_list('id', 'fen')}
    return render(request, 'index.html', context)


def add_board(request):
    white_hash = random.getrandbits(32)
    black_hash = random.getrandbits(32)
    new_board = ChessBoard.objects.create(
        white=white_hash,
        black=black_hash,
    )

    now = datetime.datetime.now()
    PGN.objects.create(
        id=new_board.id,
        event='???',
        site='???',
        date=now.strftime('%Y.%m.%d'),
        round='???',
        white=request.POST.get('white'),
        black=request.POST.get('black'),
        result='*',
    )

    response = {
        'chess_game_id': ChessBoard.objects.latest('id').id,
        'white_hash': white_hash,
        'black_hash': black_hash,
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


def update_boards(request):
    response = dict()
    try:
        response['ChessBoards'] =  {board.id: board.fen for board in ChessBoard.objects.all()}
    except Exception:
        response['status'] = 'fail'
    else:
        response['status'] = 'successful'
    return HttpResponse(json.dumps(response), content_type='application/json')


def get_fen(request, board_id):
    response = dict()
    try:
        response['FEN'] = ChessBoard.objects.get(id=board_id).fen
    except Exception:
        response['status'] = 'fail'
    else:
        response['status'] = 'successful'
    return JsonResponse(response)


def move(request, player_hash, move_uci):
    response = dict()
    try:
        board_obj = ChessBoard.objects.get(Q(white__exact=player_hash) | Q(black__exact=player_hash))
    except Exception:
        response['status'] = 'fail'
        response['message'] = 'No user with such hash ({}) was found'.format(player_hash)
        return JsonResponse(response)

    board = chess.Board(board_obj.fen)
    move = chess.Move.from_uci(move_uci)

    if move in board.legal_moves:
        pgn_obj = PGN.objects.get(id=board_obj.id)
        pgn_obj.moves += (((board.fen().split()[-1] + '.') if board.turn == chess.WHITE else '') +
                          chess.Board.san(chess.Board(board_obj.fen), move) + ' ')

        board.push(move)
        if board.is_game_over():
            pgn_obj.result = board.result()
            ChessBoard.objects.filter(id=board_obj.id).delete()
        else:
            board_obj.fen = board.fen()
            board_obj.save()

        pgn_obj.save()

        response['status'] = 'successful'
    else:
        response['status'] = 'fail'
        response['message'] = 'Invalid move ({})'.format(move_uci)

    return JsonResponse(response)


def get_report(request, board_id):
    response = dict()
    try:
        pgn_obj = PGN.objects.get(id=board_id)
        response['data'] = {
            'event': pgn_obj.event,
            'site': pgn_obj.site,
            'date': pgn_obj.date,
            'round': pgn_obj.round,
            'white': pgn_obj.white,
            'black': pgn_obj.black,
            'result': pgn_obj.result,
            'half-moves': pgn_obj.moves,
        }
    except Exception:
        response['status'] = 'fail'
    else:
        response['status'] = 'successful'

    return JsonResponse(response)

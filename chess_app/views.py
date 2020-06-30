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
        old_fen = board_obj.fen
        board.push(move)
        board_obj.fen = board.fen()
        pgn_obj = PGN.objects.get(id=board_obj.id)
        print(pgn_obj.moves)
        pgn_obj.moves += (((board.fen().split()[-1]+'.') if board.fen().split()[1] == 'b' else '') +
                            chess.Board.san(chess.Board(old_fen), move) + ' ')
        pgn_obj.save()
        board_obj.save()

        if board.is_game_over():
            board_obj.result = board.result()
            ChessBoard.objects.filter(id=board_obj.id).delete()

            response['status'] = 'successful'
            return JsonResponse(response)

        response['status'] = 'successful'
    else:
        response['status'] = 'fail'
        response['message'] = 'Invalid move ({})'.format(move_uci)

    return JsonResponse(response)


def get_report(request, board_id):
    pgn_obj = PGN.objects.get(id=board_id)
    response = {
        'event': pgn_obj.event,
        'site': pgn_obj.site,
        'date': pgn_obj.date,
        'round': pgn_obj.round,
        'white': pgn_obj.white,
        'black': pgn_obj.black,
        'result': pgn_obj.result,
        'half-moves': pgn_obj.moves,
    }
    return JsonResponse(response)

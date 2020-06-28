from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import datetime
import json

from chess_app.models import ChessBoard


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
    ChessBoard.objects.create(pgn_meta='\n'.join([event, site, date, round, white_player, black_player]))
    response = dict()
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
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

import json

from main.models import ChessBoard


def index(request):
    context = {'ChessBoards': ChessBoard.objects.values_list('id', 'fen')}
    return render(request, 'index.html', context)


def add_board(request):
    ChessBoard.objects.create()
    response = dict()
    return HttpResponse(json.dumps(response), content_type='application/json')


def update_boards(request):
    chess_boards = ChessBoard.objects.all()
    response = {'ChessBoards': dict()}
    for board in chess_boards:
        response['ChessBoards'][board.id] = board.fen
    return HttpResponse(json.dumps(response), content_type='application/json')

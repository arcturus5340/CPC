from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

import json

from main.models import ChessBoard


def index(request):
    context = {'ChessBoards': ChessBoard.objects.values_list('id', flat=True)}
    return render(request, 'index.html', context)


def add_board(request):
    ChessBoard.objects.create()
    response = dict()
    context = {'ChessBoards': ChessBoard.objects.values_list('id', flat=True)}
    response['ChessBoards'] = render_to_string('chess_boards.html', context)
    print(response['ChessBoards'])
    return HttpResponse(json.dumps(response), content_type='application/json')


def update_boards(request):
    chess_boards = ChessBoard.objects.all()
    response = {'ChessBoards': dict()}
    for board in chess_boards:
        response['ChessBoards'][board.id] = board.fen
    return HttpResponse(json.dumps(response), content_type='application/json')

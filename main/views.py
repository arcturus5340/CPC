from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string

import json
import random
import time

import chess

from main.models import ChessBoard


def index(request):
    chess_boards = ChessBoard.objects.all()
    context = {'ChessBoards': []}
    for board_obj in chess_boards:
        context['ChessBoards'].append(board_obj.id)
    return render(request, 'index.html', context)


def add_board(request):
    ChessBoard.objects.create()
    return redirect(index)


def get_boards(request):
    chess_boards = ChessBoard.objects.all()
    response = {'ChessBoards': dict()}
    for board in chess_boards:
        response['ChessBoards'][board.id] = board.fen
    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')

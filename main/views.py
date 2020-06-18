from django.shortcuts import render
from django.http import HttpResponse

import json
import random

import chess


chess_board = chess.Board()


def index(request):
    return render(request, 'index.html')


def make_random_move(request):
    global chess_board
    legal_moves = list(chess_board.legal_moves)
    if chess_board.is_game_over():
        chess_board = chess.Board()
        return render(request, 'index.html')
    random_index = random.randint(0, len(legal_moves)-1)
    chess_board.push(legal_moves[random_index])
    response = {'FEN': chess_board.fen()}
    return HttpResponse(json.dumps(response), content_type='application/json')
